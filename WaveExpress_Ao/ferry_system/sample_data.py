"""
Sample data to populate the ferry system database for testing.
Run this script with:
    python manage.py shell < ferry_system/sample_data.py
"""

import os
import django
import datetime
from django.utils import timezone
from django.contrib.auth.models import User

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WaveExpress_Ao.settings')
django.setup()

# Now we can import models
from ferry_system.models import (
    Ferry, Port, Route, Schedule, Passenger, Ticket, 
    Reservation, Payment, Staff, FerryAssignment
)

def create_sample_data():
    print("Creating sample data for the Ferry System...")
    
    # Create admin user if not exists
    try:
        admin_user = User.objects.get(username='admin')
        print("Admin user already exists.")
    except User.DoesNotExist:
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print("Created admin user.")
    
    # Create staff users
    staff_user1, created = User.objects.get_or_create(
        username='staff1',
        defaults={
            'email': 'staff1@example.com',
            'first_name': 'Staff',
            'last_name': 'One'
        }
    )
    if created:
        staff_user1.set_password('staff123')
        staff_user1.save()
        print("Created staff user 1.")
    
    staff_user2, created = User.objects.get_or_create(
        username='staff2',
        defaults={
            'email': 'staff2@example.com',
            'first_name': 'Staff',
            'last_name': 'Two'
        }
    )
    if created:
        staff_user2.set_password('staff123')
        staff_user2.save()
        print("Created staff user 2.")
    
    # Create passenger users
    passenger_user1, created = User.objects.get_or_create(
        username='passenger1',
        defaults={
            'email': 'passenger1@example.com',
            'first_name': 'Juan',
            'last_name': 'Dela Cruz'
        }
    )
    if created:
        passenger_user1.set_password('pass123')
        passenger_user1.save()
        print("Created passenger user 1.")
    
    passenger_user2, created = User.objects.get_or_create(
        username='passenger2',
        defaults={
            'email': 'passenger2@example.com',
            'first_name': 'Maria',
            'last_name': 'Santos'
        }
    )
    if created:
        passenger_user2.set_password('pass123')
        passenger_user2.save()
        print("Created passenger user 2.")
    
    # Create ferries
    ferry1, created = Ferry.objects.get_or_create(
        ferry_name='Cebu Voyager',
        defaults={
            'capacity': 200,
            'model': 'FastCraft 2000',
            'registration_number': 'FE-12345'
        }
    )
    if created:
        print("Created ferry: Cebu Voyager")
    
    ferry2, created = Ferry.objects.get_or_create(
        ferry_name='Manila Breeze',
        defaults={
            'capacity': 150,
            'model': 'Transit 1500',
            'registration_number': 'FE-67890'
        }
    )
    if created:
        print("Created ferry: Manila Breeze")
    
    ferry3, created = Ferry.objects.get_or_create(
        ferry_name='Bohol Explorer',
        defaults={
            'capacity': 180,
            'model': 'Island Hopper',
            'registration_number': 'FE-24680'
        }
    )
    if created:
        print("Created ferry: Bohol Explorer")
    
    # Create ports
    port1, created = Port.objects.get_or_create(
        port_name='Cebu Port',
        defaults={'location': 'Cebu City, Cebu'}
    )
    if created:
        print("Created port: Cebu Port")
    
    port2, created = Port.objects.get_or_create(
        port_name='Manila North Harbor',
        defaults={'location': 'Manila, Metro Manila'}
    )
    if created:
        print("Created port: Manila North Harbor")
    
    port3, created = Port.objects.get_or_create(
        port_name='Tagbilaran Port',
        defaults={'location': 'Tagbilaran City, Bohol'}
    )
    if created:
        print("Created port: Tagbilaran Port")
        
    port4, created = Port.objects.get_or_create(
        port_name='Cagayan de Oro Port',
        defaults={'location': 'Cagayan de Oro City, Misamis Oriental'}
    )
    if created:
        print("Created port: Cagayan de Oro Port")
        
    port5, created = Port.objects.get_or_create(
        port_name='Batangas Port',
        defaults={'location': 'Batangas City, Batangas'}
    )
    if created:
        print("Created port: Batangas Port")
    
    # Create routes
    route1, created = Route.objects.get_or_create(
        route_name='Cebu-Bohol Route',
        defaults={
            'departure_port': port1,
            'arrival_port': port3,
            'distance': 75.0
        }
    )
    if created:
        print("Created route: Cebu-Bohol Route")
    
    route2, created = Route.objects.get_or_create(
        route_name='Bohol-Cebu Route',
        defaults={
            'departure_port': port3,
            'arrival_port': port1,
            'distance': 75.0
        }
    )
    if created:
        print("Created route: Bohol-Cebu Route")
    
    route3, created = Route.objects.get_or_create(
        route_name='Manila-Cebu Route',
        defaults={
            'departure_port': port2,
            'arrival_port': port1,
            'distance': 562.0
        }
    )
    if created:
        print("Created route: Manila-Cebu Route")
        
    route4, created = Route.objects.get_or_create(
        route_name='Cebu-Manila Route',
        defaults={
            'departure_port': port1,
            'arrival_port': port2,
            'distance': 562.0
        }
    )
    if created:
        print("Created route: Cebu-Manila Route")
        
    route5, created = Route.objects.get_or_create(
        route_name='Manila-Batangas Route',
        defaults={
            'departure_port': port2,
            'arrival_port': port5,
            'distance': 110.0
        }
    )
    if created:
        print("Created route: Manila-Batangas Route")
    
    # Create schedules
    tomorrow = timezone.now() + datetime.timedelta(days=1)
    departure_time1 = datetime.datetime(
        tomorrow.year, tomorrow.month, tomorrow.day, 8, 0, 0,
        tzinfo=timezone.get_current_timezone()
    )
    arrival_time1 = departure_time1 + datetime.timedelta(hours=2)  # Cebu to Bohol takes about 2 hours
    
    schedule1, created = Schedule.objects.get_or_create(
        ferry=ferry1,
        route=route1,
        departure_time=departure_time1,
        defaults={
            'arrival_time': arrival_time1,
            'price': 800.00,  # PHP price
            'reserve': True
        }
    )
    if created:
        print(f"Created schedule: {schedule1}")
    
    day_after_tomorrow = timezone.now() + datetime.timedelta(days=2)
    departure_time2 = datetime.datetime(
        day_after_tomorrow.year, day_after_tomorrow.month, day_after_tomorrow.day, 10, 0, 0,
        tzinfo=timezone.get_current_timezone()
    )
    arrival_time2 = departure_time2 + datetime.timedelta(hours=2)  # Bohol to Cebu takes about 2 hours
    
    schedule2, created = Schedule.objects.get_or_create(
        ferry=ferry2,
        route=route2,
        departure_time=departure_time2,
        defaults={
            'arrival_time': arrival_time2,
            'price': 800.00,  # PHP price
            'reserve': False
        }
    )
    if created:
        print(f"Created schedule: {schedule2}")
        
    # Manila to Cebu overnight ferry
    in_three_days = timezone.now() + datetime.timedelta(days=3)
    departure_time3 = datetime.datetime(
        in_three_days.year, in_three_days.month, in_three_days.day, 18, 0, 0,
        tzinfo=timezone.get_current_timezone()
    )
    arrival_time3 = departure_time3 + datetime.timedelta(hours=22)  # Manila to Cebu takes about 22 hours
    
    schedule3, created = Schedule.objects.get_or_create(
        ferry=ferry3,
        route=route3,
        departure_time=departure_time3,
        defaults={
            'arrival_time': arrival_time3,
            'price': 2500.00,  # PHP price for longer route
            'reserve': True
        }
    )
    if created:
        print(f"Created schedule: {schedule3}")
    
    # Create staff members
    staff1, created = Staff.objects.get_or_create(
        user=staff_user1,
        defaults={
            'staff_name': 'Antonio Reyes',
            'position': 'Captain',
            'contact_number': '09171234567',
            'email': 'staff1@example.com'
        }
    )
    if created:
        print("Created staff member: Antonio Reyes")
    
    staff2, created = Staff.objects.get_or_create(
        user=staff_user2,
        defaults={
            'staff_name': 'Elena Marasigan',
            'position': 'Supervisor',
            'contact_number': '09189876543',
            'email': 'staff2@example.com'
        }
    )
    if created:
        print("Created staff member: Elena Marasigan")
    
    # Create passengers
    passenger1, created = Passenger.objects.get_or_create(
        user=passenger_user1,
        defaults={
            'passenger_name': 'Juan Dela Cruz',
            'contact_number': '09175551234',
            'address': '123 Rizal Street, Makati City',
            'email': 'juan.delacruz@example.com'
        }
    )
    if created:
        print("Created passenger: Juan Dela Cruz")
    
    passenger2, created = Passenger.objects.get_or_create(
        user=passenger_user2,
        defaults={
            'passenger_name': 'Maria Santos',
            'contact_number': '09185557890',
            'address': '456 Bonifacio Avenue, Quezon City',
            'email': 'maria.santos@example.com'
        }
    )
    if created:
        print("Created passenger: Maria Santos")
    
    # Create ferry assignments
    assignment1, created = FerryAssignment.objects.get_or_create(
        ferry=ferry1,
        schedule=schedule1,
        staff=staff1,
        defaults={'assignment_date': timezone.now()}
    )
    if created:
        print(f"Created ferry assignment: {assignment1}")
    
    assignment2, created = FerryAssignment.objects.get_or_create(
        ferry=ferry2,
        schedule=schedule2,
        staff=staff2,
        defaults={'assignment_date': timezone.now()}
    )
    if created:
        print(f"Created ferry assignment: {assignment2}")
    
    # Create tickets (Transaction 1: Passenger buys a ticket)
    ticket1, created = Ticket.objects.get_or_create(
        schedule=schedule1,
        passenger=passenger1,
        defaults={
            'purchase_date': timezone.now(),
            'seat_number': 'A1',
            'ticket_status': 'ACTIVE',
            'payment_status': 'PAID'
        }
    )
    if created:
        print(f"Created ticket: {ticket1}")
    
    # Create reservation (Transaction 2: A passenger reserves a ticket)
    reservation1, created = Reservation.objects.get_or_create(
        schedule=schedule1,
        passenger=passenger2,
        defaults={
            'date_of_reservation': timezone.now(),
            'status': 'PENDING'
        }
    )
    if created:
        print(f"Created reservation: {reservation1}")
    
    # Create payments (Transaction 4: A passenger pays for ticket/reservation)
    payment1, created = Payment.objects.get_or_create(
        ticket=ticket1,
        defaults={
            'amount': 800.00,  # PHP price
            'payment_date': timezone.now(),
            'payment_method': 'CREDIT_CARD',
            'payment_status': 'COMPLETED',
            'transaction_reference': 'TXN-1234567890'
        }
    )
    if created:
        print(f"Created payment: {payment1}")
    
    payment2, created = Payment.objects.get_or_create(
        reservation=reservation1,
        defaults={
            'amount': 400.00,  # Deposit for reservation (50% of ticket price)
            'payment_date': timezone.now(),
            'payment_method': 'BANK_TRANSFER',
            'payment_status': 'PENDING',
            'transaction_reference': 'TXN-0987654321'
        }
    )
    if created:
        print(f"Created payment: {payment2}")
    
    print("Sample data creation completed!")

if __name__ == "__main__":
    create_sample_data()
