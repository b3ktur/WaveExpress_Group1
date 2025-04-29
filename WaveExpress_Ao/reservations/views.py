from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction, connection
from django.utils import timezone
from decimal import Decimal
import datetime
from .models import Destination, Schedule, Reservation
from .forms import ReservationForm, ScheduleSearchForm

@login_required
def schedule_search(request):
    """Search for available schedules"""
    today = datetime.date.today()
    
    if request.method == 'POST':
        form = ScheduleSearchForm(request.POST)
        if form.is_valid():
            origin = form.cleaned_data['origin']
            destination_name = form.cleaned_data['destination']
            departure_date = form.cleaned_data['departure_date']
            passengers = form.cleaned_data['passengers']
            
            # Store search parameters in session for later use
            request.session['search_params'] = {
                'origin': origin,
                'destination': destination_name,
                'departure_date': departure_date.strftime('%Y-%m-%d'),
                'passengers': passengers
            }
            
            # Call stored procedure to find schedules
            with connection.cursor() as cursor:
                # Check if stored procedure exists, if not, create it
                cursor.execute("""
                    CREATE PROCEDURE IF NOT EXISTS FindAvailableSchedules(
                        IN p_origin VARCHAR(100),
                        IN p_destination VARCHAR(100),
                        IN p_departure_date DATE,
                        IN p_passengers INT
                    )
                    BEGIN
                        SELECT s.id, s.origin, d.name as destination_name, 
                               s.departure_date, s.departure_time, s.price, s.available_seats
                        FROM reservations_schedule s
                        JOIN reservations_destination d ON s.destination_id = d.id
                        WHERE s.origin LIKE CONCAT('%', p_origin, '%')
                        AND d.name LIKE CONCAT('%', p_destination, '%')
                        AND s.departure_date = p_departure_date
                        AND s.available_seats >= p_passengers;
                    END
                """)
                
                # Call the stored procedure
                cursor.callproc('FindAvailableSchedules', [
                    origin, 
                    destination_name, 
                    departure_date,
                    passengers
                ])
                
                # Get results
                schedules_data = cursor.fetchall()
            
            # Process the raw data into schedule objects
            schedules = []
            for row in schedules_data:
                schedule = {
                    'id': row[0],
                    'origin': row[1],
                    'destination_name': row[2],
                    'departure_date': row[3],
                    'departure_time': row[4],
                    'price': row[5],
                    'available_seats': row[6]
                }
                schedules.append(schedule)
            
            if not schedules:
                messages.info(request, "No schedules found for your search criteria.")
            
            return render(request, 'reservations/schedule_list.html', {
                'schedules': schedules,
                'search_params': request.session['search_params']
            })
    else:
        form = ScheduleSearchForm()
    
    return render(request, 'reservations/schedule_search.html', {
        'form': form,
        'today': today
    })

@login_required
def create_reservation(request, schedule_id):
    """Create a new reservation"""
    schedule = get_object_or_404(Schedule, pk=schedule_id)
    
    # Get search parameters from session
    search_params = request.session.get('search_params', {})
    passengers_count = int(search_params.get('passengers', 1))
    
    # Calculate price (without service fee)
    total_price = schedule.price * passengers_count
    
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Create the reservation
                    reservation = form.save(commit=False)
                    reservation.user = request.user
                    reservation.schedule = schedule
                    reservation.number_of_passengers = passengers_count
                    reservation.total_price = total_price
                    reservation.status = 'confirmed'  # Auto-confirm
                    
                    # Update available seats
                    if schedule.available_seats >= passengers_count:
                        schedule.available_seats -= passengers_count
                        schedule.save()
                    else:
                        raise ValueError("Not enough seats available for this schedule")
                    
                    # Save the reservation
                    reservation.save()
                    
                    messages.success(request, "Your reservation has been created successfully!")
                    return redirect('my_reservations')
            except ValueError as e:
                messages.error(request, str(e))
                return redirect('schedule_search')
    else:
        form = ReservationForm(initial={'number_of_passengers': passengers_count})
    
    context = {
        'schedule': schedule,
        'form': form,
        'search_params': search_params,
        'total_price': total_price
    }
    
    return render(request, 'reservations/create_reservation.html', context)

@login_required
def my_reservations(request):
    """View user's reservations"""
    reservations = Reservation.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'reservations/my_reservations.html', {'reservations': reservations})
