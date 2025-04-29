from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from django.urls import reverse
from django.db.models import Q

from .models import Schedule, Ticket, Payment, Passenger, Port
from .ticket_forms import TicketPurchaseForm, TicketPaymentForm

import uuid
import datetime

def schedule_list(request):
    """View to display available schedules for ticket purchase"""
    ports = Port.objects.all().order_by('port_name')
    
    # Get filter parameters from request
    departure_port = request.GET.get('departure_port')
    arrival_port = request.GET.get('arrival_port')
    departure_date = request.GET.get('departure_date')
    
    # Start with all schedules in the future
    schedules = Schedule.objects.filter(
        departure_time__gt=timezone.now()
    ).order_by('departure_time')
    
    # Apply filters if provided
    if departure_port:
        schedules = schedules.filter(route__departure_port_id=departure_port)
    
    if arrival_port:
        schedules = schedules.filter(route__arrival_port_id=arrival_port)
    
    if departure_date:
        try:
            date_obj = datetime.datetime.strptime(departure_date, '%Y-%m-%d').date()
            schedules = schedules.filter(
                departure_time__year=date_obj.year,
                departure_time__month=date_obj.month,
                departure_time__day=date_obj.day
            )
        except ValueError:
            # Invalid date format, ignore this filter
            pass
    
    context = {
        'schedules': schedules,
        'ports': ports,
    }
    
    return render(request, 'ferry_system/schedule_list.html', context)

@login_required
def buy_ticket(request, schedule_id):
    """View to purchase a ticket for a specific schedule"""
    schedule = get_object_or_404(Schedule, pk=schedule_id)
    
    # Check if schedule is in the past
    if schedule.departure_time < timezone.now():
        messages.error(request, "Cannot purchase tickets for past schedules.")
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
    tickets_sold = Ticket.objects.filter(
        schedule=schedule,
        ticket_status='ACTIVE'
    ).count()
    available_capacity = schedule.ferry.capacity - tickets_sold
    
    if available_capacity <= 0:
        messages.error(request, "Sorry, this schedule is fully booked.")
        return redirect('ferry_system:schedule_list')
    
    if request.method == 'POST':
        form = TicketPurchaseForm(request.POST, schedule=schedule, passenger=passenger)
        
        if form.is_valid():
            # Create the ticket
            ticket = form.save(commit=False)
            ticket.schedule = schedule
            ticket.passenger = passenger
            ticket.purchase_date = timezone.now()
            ticket.ticket_status = 'ACTIVE'
            ticket.payment_status = 'UNPAID'
            
            # If seat number is not provided, assign one automatically
            if not ticket.seat_number:
                # This is a simple approach - in a real app, you might have a more sophisticated seat assignment system
                existing_seats = Ticket.objects.filter(
                    schedule=schedule,
                    ticket_status='ACTIVE'
                ).values_list('seat_number', flat=True)
                
                # Generate a simple seat number (A1, A2, etc.)
                for row in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    for num in range(1, 31):
                        seat = f"{row}{num}"
                        if seat not in existing_seats:
                            ticket.seat_number = seat
                            break
                    if ticket.seat_number:
                        break
            
            ticket.save()
            
            # Redirect to payment page
            return redirect('ferry_system:pay_ticket', ticket_id=ticket.ticket_id)
    else:
        form = TicketPurchaseForm(schedule=schedule, passenger=passenger)
    
    context = {
        'form': form,
        'schedule': schedule,
        'available_capacity': available_capacity,
    }
    
    return render(request, 'ferry_system/ticket/buy_ticket.html', context)

@login_required
def pay_ticket(request, ticket_id):
    """View to handle payment for a purchased ticket"""
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    
    # Security check: ensure the ticket belongs to the current user
    if ticket.passenger.user != request.user:
        messages.error(request, "You don't have permission to pay for this ticket.")
        return redirect('ferry_system:my_tickets')
    
    # Check if ticket is already paid
    if ticket.payment_status == 'PAID':
        messages.info(request, "This ticket has already been paid for.")
        return redirect('ferry_system:ticket_detail', ticket_id=ticket.ticket_id)
    
    if request.method == 'POST':
        form = TicketPaymentForm(request.POST)
        
        if form.is_valid():
            # Create the payment record
            payment = form.save(commit=False)
            payment.ticket = ticket
            payment.amount = ticket.schedule.price
            payment.payment_date = timezone.now()
            payment.payment_status = 'COMPLETED'
            
            # Generate a transaction reference
            payment.transaction_reference = f"TXN-{uuid.uuid4().hex[:12].upper()}"
            
            payment.save()
            
            # Update ticket payment status
            ticket.payment_status = 'PAID'
            ticket.save()
            
            messages.success(request, "Payment completed successfully!")
            return redirect('ferry_system:ticket_confirmation', ticket_id=ticket.ticket_id)
    else:
        form = TicketPaymentForm()
    
    context = {
        'form': form,
        'ticket': ticket,
    }
    
    return render(request, 'ferry_system/ticket/payment.html', context)

@login_required
def ticket_confirmation(request, ticket_id):
    """View to display ticket confirmation after successful payment"""
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    
    # Security check: ensure the ticket belongs to the current user
    if ticket.passenger.user != request.user:
        messages.error(request, "You don't have permission to view this ticket.")
        return redirect('ferry_system:my_tickets')
    
    # Get the payment information
    try:
        payment = Payment.objects.get(ticket=ticket)
    except Payment.DoesNotExist:
        payment = None
    
    context = {
        'ticket': ticket,
        'payment': payment,
    }
    
    return render(request, 'ferry_system/ticket/confirmation.html', context)

@login_required
def ticket_detail(request, ticket_id):
    """View to display ticket details"""
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    
    # Security check: ensure the ticket belongs to the current user
    if ticket.passenger.user != request.user:
        messages.error(request, "You don't have permission to view this ticket.")
        return redirect('ferry_system:my_tickets')
    
    # Get the payment information
    try:
        payment = Payment.objects.get(ticket=ticket)
    except Payment.DoesNotExist:
        payment = None
    
    context = {
        'ticket': ticket,
        'payment': payment,
    }
    
    return render(request, 'ferry_system/ticket/detail.html', context)

@login_required
def my_tickets(request):
    """View to display the current user's tickets"""
    try:
        passenger = Passenger.objects.get(user=request.user)
        tickets = Ticket.objects.filter(passenger=passenger).order_by('-purchase_date')
    except Passenger.DoesNotExist:
        tickets = []
    
    context = {
        'tickets': tickets,
    }
    
    return render(request, 'ferry_system/ticket/my_tickets.html', context)

@login_required
def print_ticket(request, ticket_id):
    """View to print a ticket"""
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    
    # Security check: ensure the ticket belongs to the current user
    if ticket.passenger.user != request.user:
        messages.error(request, "You don't have permission to print this ticket.")
        return redirect('ferry_system:my_tickets')
    
    context = {
        'ticket': ticket,
    }
    
    return render(request, 'ferry_system/ticket/print_ticket.html', context)

@login_required
def cancel_ticket(request, ticket_id):
    """View to cancel a ticket"""
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    
    # Security check: ensure the ticket belongs to the current user
    if ticket.passenger.user != request.user:
        messages.error(request, "You don't have permission to cancel this ticket.")
        return redirect('ferry_system:my_tickets')
    
    # Check if ticket can be cancelled
    if ticket.ticket_status != 'ACTIVE':
        messages.error(request, "This ticket cannot be cancelled.")
        return redirect('ferry_system:ticket_detail', ticket_id=ticket.ticket_id)
    
    # Check if departure time is within 24 hours
    if ticket.schedule.departure_time - timezone.now() < datetime.timedelta(hours=24):
        messages.error(request, "Tickets cannot be cancelled within 24 hours of departure.")
        return redirect('ferry_system:ticket_detail', ticket_id=ticket.ticket_id)
    
    # Cancel the ticket
    ticket.ticket_status = 'CANCELLED'
    ticket.save()
    
    # If the ticket was paid, create a refund
    if ticket.payment_status == 'PAID':
        try:
            payment = Payment.objects.get(ticket=ticket)
            # Create a refund record
            refund = Payment.objects.create(
                ticket=ticket,
                amount=payment.amount,
                payment_date=timezone.now(),
                payment_method=payment.payment_method,
                payment_status='COMPLETED',
                transaction_reference=f"REF-{uuid.uuid4().hex[:12].upper()}"
            )
            ticket.payment_status = 'REFUNDED'
            ticket.save()
        except Payment.DoesNotExist:
            pass
    
    messages.success(request, "Your ticket has been cancelled successfully.")
    return redirect('ferry_system:my_tickets')
