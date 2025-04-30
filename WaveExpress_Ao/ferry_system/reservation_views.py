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
    try:
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
    except Exception as e:
        messages.error(request, f"Error accessing schedule: {str(e)}")
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
        try:
            # Add schedule_id to POST data to ensure it's included in the form
            post_data = request.POST.copy()
            post_data['schedule'] = schedule.pk
            
            form = ReservationForm(post_data, schedule=schedule, passenger=passenger)
            
            if form.is_valid():
                reservation_type = request.POST.get('reservation_type', 'pay_now')
                
                # Create the reservation with explicit schedule assignment
                reservation = form.save(commit=False)
                reservation.schedule = schedule  # Explicitly assign the schedule object
                reservation.passenger = passenger
                reservation.date_of_reservation = timezone.now()
                reservation.status = 'PENDING'
                reservation.save()
                
                # Set an expiration time (24 hours from now) for pending reservations
                expiry_time = timezone.now() + datetime.timedelta(hours=24)
                request.session['reservation_expiry'] = expiry_time.strftime('%Y-%m-%d %H:%M:%S')
                
                if reservation_type == 'pay_later':
                    # Add a confirmation message for Pay Later option
                    messages.success(request, f"Your reservation has been created successfully! You have 24 hours (until {expiry_time.strftime('%b %d, %Y %I:%M %p')}) to complete the payment.")
                    return redirect('ferry_system:my_reservations')
                else:  # pay_now option
                    # Skip the payment form and redirect directly to the "working on it" page
                    messages.info(request, "Redirecting to our payment system...")
                    return redirect('ferry_system:payment_in_progress', reservation_id=reservation.reservation_id)
            else:
                # If form is not valid, show error messages
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"Error in {field}: {error}")
        except Exception as e:
            messages.error(request, f"Error creating reservation: {str(e)}")
            return redirect('ferry_system:schedule_list')
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
            # Redirect to the "Working on it" page
            return redirect('ferry_system:payment_in_progress', reservation_id=reservation.reservation_id)
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
def payment_in_progress(request, reservation_id):
    """View to show 'Working on it' page for payments"""
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    
    # Security check: ensure the reservation belongs to the current user
    if reservation.passenger.user != request.user:
        messages.error(request, "You don't have permission to view this page.")
        return redirect('ferry_system:my_reservations')
    
    context = {
        'reservation': reservation,
    }
    
    return render(request, 'ferry_system/reservation/payment_in_progress.html', context)

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
        'now': timezone.now(),
    }
    
    return render(request, 'ferry_system/reservation/detail.html', context)

@login_required
def my_reservations(request):
    """View to display the current user's reservations"""
    try:
        passenger = Passenger.objects.get(user=request.user)
        
        # Check for expired PENDING reservations (older than 24 hours)
        expired_cutoff = timezone.now() - datetime.timedelta(hours=24)
        expired_reservations = Reservation.objects.filter(
            passenger=passenger, 
            status='PENDING',
            date_of_reservation__lt=expired_cutoff
        )
        
        # Auto-cancel expired reservations
        if expired_reservations.exists():
            count = expired_reservations.update(status='CANCELLED')
            if count > 0:
                messages.warning(request, f"{count} pending reservation(s) have been automatically cancelled because the 24-hour payment window has passed.")
        
        # Get all reservations for the passenger
        reservations = Reservation.objects.filter(passenger=passenger).order_by('-date_of_reservation')
        
    except Passenger.DoesNotExist:
        # Create a passenger record if it doesn't exist
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        passenger = Passenger.objects.create(
            user=request.user,
            passenger_name=f"{request.user.first_name} {request.user.last_name}",
            contact_number=profile.phone_number or '',
            address=profile.address or '',
            email=request.user.email
        )
        reservations = []
    
    # Get reservation expiry time from session if it exists
    reservation_expiry = None
    if 'reservation_expiry' in request.session:
        try:
            expiry_str = request.session['reservation_expiry']
            reservation_expiry = datetime.datetime.strptime(expiry_str, '%Y-%m-%d %H:%M:%S')
            # Make it timezone aware
            reservation_expiry = timezone.make_aware(reservation_expiry)
        except Exception as e:
            print(f"Error parsing reservation expiry: {str(e)}")
    
    # Add 'now' to context for template comparison
    context = {
        'reservations': reservations,
        'now': timezone.now(),
        'reservation_expiry': reservation_expiry,
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
