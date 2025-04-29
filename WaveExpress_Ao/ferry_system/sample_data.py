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
            'first_name': 'John',
            'last_name': 'Doe'
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
            'first_name': 'Jane',
            'last_name': 'Smith'
        }
    )
    if created:
        passenger_user2.set_password('pass123')
        passenger_user2.save()
        print("Created passenger user 2.")
    
    # Create ferries
    ferry1, created = Ferry.objects.get_or_create(
        ferry_name='Ocean Explorer',
        defaults={
            'capacity': 200,
            'model': 'Cruise 2000',
            'registration_number': 'FE-12345'
        }
    )
    if created:
        print("Created ferry: Ocean Explorer")
    
    ferry2, created = Ferry.objects.get_or_create(
        ferry_name='Island Hopper',
        defaults={
            'capacity': 150,
            'model': 'Transit 1500',
            'registration_number': 'FE-67890'
        }
    )
    if created:
        print("Created ferry: Island Hopper")
    
    # Create ports
    port1, created = Port.objects.get_or_create(
        port_name='North Harbor',
        defaults={'location': 'Northern City'}
    )
    if created:
        print("Created port: North Harbor")
    
    port2, created = Port.objects.get_or_create(
        port_name='South Bay',
        defaults={'location': 'Southern City'}
    )
    if created:
        print("Created port: South Bay")
    
    port3, created = Port.objects.get_or_create(
        port_name='East Point',
        defaults={'location': 'Eastern City'}
    )
    if created:
        print("Created port: East Point")
    
    # Create routes
    route1, created = Route.objects.get_or_create(
        route_name='Northern Route',
        defaults={
            'departure_port': port1,
            'arrival_port': port2,
            'distance': 120.5
        }
    )
    if created:
        print("Created route: Northern Route")
    
    route2, created = Route.objects.get_or_create(
        route_name='Southern Route',
        defaults={
            'departure_port': port2,
            'arrival_port': port1,
            'distance': 120.5
        }
    )
    if created:
        print("Created route: Southern Route")
    
    route3, created = Route.objects.get_or_create(
        route_name='Eastern Route',
        defaults={
            'departure_port': port1,
            'arrival_port': port3,
            'distance': 85.0
        }
    )
    if created:
        print("Created route: Eastern Route")
    
    # Create schedules
    tomorrow = timezone.now() + datetime.timedelta(days=1)
    departure_time1 = datetime.datetime(
        tomorrow.year, tomorrow.month, tomorrow.day, 8, 0, 0,
        tzinfo=timezone.get_current_timezone()
    )
    arrival_time1 = departure_time1 + datetime.timedelta(hours=3)
    
    schedule1, created = Schedule.objects.get_or_create(
        ferry=ferry1,
        route=route1,
        departure_time=departure_time1,
        defaults={
            'arrival_time': arrival_time1,
            'price': 50.00,
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
    arrival_time2 = departure_time2 + datetime.timedelta(hours=3)
    
    schedule2, created = Schedule.objects.get_or_create(
        ferry=ferry2,
        route=route2,
        departure_time=departure_time2,
        defaults={
            'arrival_time': arrival_time2,
            'price': 45.00,
            'reserve': False
        }
    )
    if created:
        print(f"Created schedule: {schedule2}")
    
    # Create staff members
    staff1, created = Staff.objects.get_or_create(
        user=staff_user1,
        defaults={
            'staff_name': 'Staff One',
            'position': 'Captain',
            'contact_number': '123-456-7890',
            'email': 'staff1@example.com'
        }
    )
    if created:
        print("Created staff member: Staff One")
    
    staff2, created = Staff.objects.get_or_create(
        user=staff_user2,
        defaults={
            'staff_name': 'Staff Two',
            'position': 'Supervisor',
            'contact_number': '098-765-4321',
            'email': 'staff2@example.com'
        }
    )
    if created:
        print("Created staff member: Staff Two")
    
    # Create passengers
    passenger1, created = Passenger.objects.get_or_create(
        user=passenger_user1,
        defaults={
            'passenger_name': 'John Doe',
            'contact_number': '111-222-3333',
            'address': '123 Main St, Anytown',
            'email': 'john.doe@example.com'
        }
    )
    if created:
        print("Created passenger: John Doe")
    
    passenger2, created = Passenger.objects.get_or_create(
        user=passenger_user2,
        defaults={
            'passenger_name': 'Jane Smith',
            'contact_number': '444-555-6666',
            'address': '456 Oak St, Anytown',
            'email': 'jane.smith@example.com'
        }
    )
    if created:
        print("Created passenger: Jane Smith")
    
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
            'amount': 50.00,
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
            'amount': 25.00,  # Deposit for reservation
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
