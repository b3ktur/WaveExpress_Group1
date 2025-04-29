from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from django.urls import reverse
from django.db.models import Q

from .models import Schedule, Reservation, Payment, Passenger, Port
from .reservation_forms import ReservationForm, ReservationPaymentForm

import uuid
import datetime

@login_required
def reserve_ticket(request, schedule_id):
    """View to reserve a ticket for a specific schedule"""
    schedule = get_object_or_404(Schedule, pk=schedule_id)
    
    # Check if schedule allows reservations
    if not schedule.reserve:
        messages.error(request, "This schedule does not allow reservations.")
        return redirect('ferry_system:schedule_list')
    
    # Check if schedule is in the past
    if schedule.departure_time < timezone.now():
        messages.error(request, "Cannot reserve tickets for past schedules.")
        return redirect('ferry_system:schedule_list')
    
    # Check if the departure is within 24 hours
    if schedule.departure_time - timezone.now() < datetime.timedelta(hours=24):
        messages.error(request, "Reservations must be made at least 24 hours before departure.")
        return redirect('ferry_system:schedule_list')
    
    # Get or create passenger record for the current user
    try:
        passenger = Passenger.objects.get(user=request.user)
    except Passenger.DoesNotExist:
        # Create a basic passenger record if it doesn't exist
        passenger = Passenger.objects.create(
            user=request.user,
            passenger_name=f"{request.user.first_name} {request.user.last_name}",
            email=request.user.email,
            contact_number="",
            address=""
        )
    
    # Calculate available capacity
    tickets_sold = Reservation.objects.filter(
        schedule=schedule,
        status__in=['PENDING', 'CONFIRMED']
    ).count()
    
    available_capacity = schedule.ferry.capacity - tickets_sold
    
    if available_capacity <= 0:
        messages.error(request, "Sorry, this schedule is fully booked.")
        return redirect('ferry_system:schedule_list')
    
    if request.method == 'POST':
        form = ReservationForm(request.POST, schedule=schedule, passenger=passenger)
        
        if form.is_valid():
            # Create the reservation
            reservation = form.save(commit=False)
            reservation.schedule = schedule
            reservation.passenger = passenger
            reservation.date_of_reservation = timezone.now()
            reservation.status = 'PENDING'
            reservation.save()
            
            # Redirect to deposit payment page
            return redirect('ferry_system:pay_reservation', reservation_id=reservation.reservation_id)
    else:
        form = ReservationForm(schedule=schedule, passenger=passenger)
    
    context = {
        'form': form,
        'schedule': schedule,
        'available_capacity': available_capacity,
    }
    
    return render(request, 'ferry_system/reservation/reserve_ticket.html', context)

@login_required
def pay_reservation(request, reservation_id):
    """View to handle payment for a reservation deposit"""
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    
    # Security check: ensure the reservation belongs to the current user
    if reservation.passenger.user != request.user:
        messages.error(request, "You don't have permission to pay for this reservation.")
        return redirect('ferry_system:my_reservations')
    
    # Check if reservation is already paid
    if Payment.objects.filter(reservation=reservation).exists():
        messages.info(request, "This reservation has already been paid for.")
        return redirect('ferry_system:reservation_detail', reservation_id=reservation.reservation_id)
    
    if request.method == 'POST':
        form = ReservationPaymentForm(
            request.POST, 
            reservation=reservation,
            schedule_price=reservation.schedule.price
        )
        
        if form.is_valid():
            # Create the payment record
            payment = form.save(commit=False)
            payment.reservation = reservation
            payment.amount = form.get_deposit_amount()
            payment.payment_date = timezone.now()
            payment.payment_status = 'COMPLETED'
            
            # Generate a transaction reference
            payment.transaction_reference = f"RES-{uuid.uuid4().hex[:12].upper()}"
            
            payment.save()
            
            # Update reservation status
            reservation.status = 'CONFIRMED'
            reservation.save()
            
            messages.success(request, "Payment completed successfully!")
            return redirect('ferry_system:reservation_confirmation', reservation_id=reservation.reservation_id)
    else:
        form = ReservationPaymentForm(
            reservation=reservation,
            schedule_price=reservation.schedule.price
        )
    
    context = {
        'form': form,
        'reservation': reservation,
        'schedule': reservation.schedule,
    }
    
    return render(request, 'ferry_system/reservation/payment.html', context)

@login_required
def reservation_confirmation(request, reservation_id):
    """View to display reservation confirmation after successful payment"""
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    
    # Security check: ensure the reservation belongs to the current user
    if reservation.passenger.user != request.user:
        messages.error(request, "You don't have permission to view this reservation.")
        return redirect('ferry_system:my_reservations')
    
    # Get the payment information
    try:
        payment = Payment.objects.get(reservation=reservation)
    except Payment.DoesNotExist:
        payment = None
    
    context = {
        'reservation': reservation,
        'payment': payment,
    }
    
    return render(request, 'ferry_system/reservation/confirmation.html', context)

@login_required
def reservation_detail(request, reservation_id):
    """View to display reservation details"""
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    
    # Security check: ensure the reservation belongs to the current user
    if reservation.passenger.user != request.user:
        messages.error(request, "You don't have permission to view this reservation.")
        return redirect('ferry_system:my_reservations')
    
    # Get the payment information
    try:
        payment = Payment.objects.get(reservation=reservation)
    except Payment.DoesNotExist:
        payment = None
    
    context = {
        'reservation': reservation,
        'payment': payment,
    }
    
    return render(request, 'ferry_system/reservation/detail.html', context)

@login_required
def my_reservations(request):
    """View to display the current user's reservations"""
    try:
        passenger = Passenger.objects.get(user=request.user)
        reservations = Reservation.objects.filter(passenger=passenger).order_by('-date_of_reservation')
    except Passenger.DoesNotExist:
        reservations = []
    
    context = {
        'reservations': reservations,
    }
    
    return render(request, 'ferry_system/reservation/my_reservations.html', context)

@login_required
def cancel_reservation(request, reservation_id):
    """View to cancel a reservation"""
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    
    # Security check: ensure the reservation belongs to the current user
    if reservation.passenger.user != request.user:
        messages.error(request, "You don't have permission to cancel this reservation.")
        return redirect('ferry_system:my_reservations')
    
    # Check if reservation can be cancelled
    if reservation.status == 'CANCELLED':
        messages.error(request, "This reservation is already cancelled.")
        return redirect('ferry_system:reservation_detail', reservation_id=reservation.reservation_id)
    
    # Check if departure time is within 48 hours
    if reservation.schedule.departure_time - timezone.now() < datetime.timedelta(hours=48):
        messages.error(request, "Reservations cannot be cancelled within 48 hours of departure.")
        return redirect('ferry_system:reservation_detail', reservation_id=reservation.reservation_id)
    
    # Cancel the reservation
    reservation.status = 'CANCELLED'
    reservation.save()
    
    # Check if there was a payment
    try:
        payment = Payment.objects.get(reservation=reservation)
        # Create a refund record
        refund = Payment.objects.create(
            reservation=reservation,
            amount=payment.amount,
            payment_date=timezone.now(),
            payment_method=payment.payment_method,
            payment_status='REFUNDED',
            transaction_reference=f"REF-{uuid.uuid4().hex[:12].upper()}"
        )
    except Payment.DoesNotExist:
        pass
    
    messages.success(request, "Your reservation has been cancelled successfully.")
    return redirect('ferry_system:my_reservations')

@login_required
def convert_to_ticket(request, reservation_id):
    """View to convert a reservation to a ticket (simplified version)"""
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    
    # Security check: ensure the reservation belongs to the current user
    if reservation.passenger.user != request.user:
        messages.error(request, "You don't have permission to manage this reservation.")
        return redirect('ferry_system:my_reservations')
    
    # Check if reservation is confirmed
    if reservation.status != 'CONFIRMED':
        messages.error(request, "Only confirmed reservations can be converted to tickets.")
        return redirect('ferry_system:reservation_detail', reservation_id=reservation.reservation_id)
    
    # Check if the schedule is still available
    if reservation.schedule.departure_time < timezone.now():
        messages.error(request, "Cannot convert reservations for past schedules.")
        return redirect('ferry_system:reservation_detail', reservation_id=reservation.reservation_id)
    
    # Get reservation payment
    try:
        reservation_payment = Payment.objects.get(reservation=reservation)
    except Payment.DoesNotExist:
        messages.error(request, "No payment found for this reservation.")
        return redirect('ferry_system:reservation_detail', reservation_id=reservation.reservation_id)
    
    # Mark the reservation as completed
    reservation.status = 'COMPLETED'
    reservation.save()
    
    messages.success(request, "Your reservation has been converted to a ticket successfully. For Transaction #2 demo purposes, we're simply marking the reservation as completed.")
    return redirect('ferry_system:reservation_detail', reservation_id=reservation.reservation_id)

# The complete_reservation_payment function has been removed as we simplified the conversion process
