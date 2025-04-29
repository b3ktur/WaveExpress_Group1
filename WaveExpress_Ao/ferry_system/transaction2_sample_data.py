from django.db import transaction
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Ferry, Port, Route, Schedule, Passenger, Staff, Reservation, Payment
import datetime
import random
import uuid

def create_sample_data():
    """Create sample data for Transaction #2: A passenger reserves a ticket"""
    
    with transaction.atomic():
        print("Creating sample data for Transaction #2...")
        
        # Create sample ferries if they don't exist
        if not Ferry.objects.exists():
            ferries = [
                {'ferry_name': 'Ocean Voyager', 'capacity': 200, 'model': 'Catamaran XL-200', 'registration_number': 'PH-FRY-001'},
                {'ferry_name': 'Island Hopper', 'capacity': 150, 'model': 'Fastcraft FC-150', 'registration_number': 'PH-FRY-002'},
                {'ferry_name': 'Wave Rider', 'capacity': 180, 'model': 'Cruiser C-180', 'registration_number': 'PH-FRY-003'},
                {'ferry_name': 'Sea Breeze', 'capacity': 120, 'model': 'Speedboat SB-120', 'registration_number': 'PH-FRY-004'},
                {'ferry_name': 'Pacific Explorer', 'capacity': 250, 'model': 'Mega Ferry MF-250', 'registration_number': 'PH-FRY-005'},
            ]
            
            for ferry_data in ferries:
                Ferry.objects.create(**ferry_data)
                print(f"Created ferry: {ferry_data['ferry_name']}")
        
        # Create sample ports if they don't exist
        if not Port.objects.exists():
            ports = [
                {'port_name': 'Manila North Harbor', 'location': 'Manila, Philippines'},
                {'port_name': 'Batangas Port', 'location': 'Batangas City, Philippines'},
                {'port_name': 'Calapan Port', 'location': 'Calapan, Oriental Mindoro, Philippines'},
                {'port_name': 'Cebu Port', 'location': 'Cebu City, Philippines'},
                {'port_name': 'Tagbilaran Port', 'location': 'Tagbilaran, Bohol, Philippines'},
                {'port_name': 'Cagayan de Oro Port', 'location': 'Cagayan de Oro, Philippines'},
                {'port_name': 'Dumaguete Port', 'location': 'Dumaguete, Negros Oriental, Philippines'},
                {'port_name': 'Iloilo Port', 'location': 'Iloilo City, Philippines'},
                {'port_name': 'Bacolod Port', 'location': 'Bacolod, Negros Occidental, Philippines'},
                {'port_name': 'Coron Port', 'location': 'Coron, Palawan, Philippines'},
            ]
            
            for port_data in ports:
                Port.objects.create(**port_data)
                print(f"Created port: {port_data['port_name']}")
        
        # Create sample routes if they don't exist
        if not Route.objects.exists():
            all_ports = Port.objects.all()
            
            # Create routes between different ports
            for departure_port in all_ports:
                for arrival_port in all_ports:
                    if departure_port != arrival_port:
                        route_name = f"{departure_port.port_name} to {arrival_port.port_name}"
                        distance = random.uniform(50, 500)  # Random distance between 50 and 500 km
                        
                        Route.objects.create(
                            route_name=route_name,
                            departure_port=departure_port,
                            arrival_port=arrival_port,
                            distance=distance
                        )
                        print(f"Created route: {route_name}")
        
        # Create sample schedules if they don't exist
        if not Schedule.objects.exists():
            all_ferries = Ferry.objects.all()
            all_routes = Route.objects.all()
            
            # Create schedules for the next 30 days
            today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            
            for day in range(1, 31):
                # Each day, create 10 random schedules
                for _ in range(10):
                    ferry = random.choice(all_ferries)
                    route = random.choice(all_routes)
                    
                    # Random departure time between 6 AM and 8 PM
                    departure_hour = random.randint(6, 20)
                    departure_minute = random.choice([0, 15, 30, 45])
                    
                    departure_time = today + datetime.timedelta(days=day, hours=departure_hour, minutes=departure_minute)
                    
                    # Calculate arrival time (1-8 hours after departure)
                    travel_hours = max(1, int(route.distance / 60))  # Assume average speed of 60 km/h
                    arrival_time = departure_time + datetime.timedelta(hours=travel_hours)
                    
                    # Random price between ₱1000 and ₱5000
                    price = random.randint(1000, 5000)
                    
                    # 50% chance of allowing reservations
                    reserve = random.choice([True, False])
                    
                    Schedule.objects.create(
                        ferry=ferry,
                        route=route,
                        departure_time=departure_time,
                        arrival_time=arrival_time,
                        price=price,
                        reserve=reserve
                    )
                    
                print(f"Created schedules for day {day}")
        
        # Create sample users and passengers if they don't exist
        if User.objects.count() < 5:
            # Create some test users
            test_users = [
                {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe', 'password': 'password123'},
                {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith', 'password': 'password123'},
                {'username': 'bob_johnson', 'email': 'bob@example.com', 'first_name': 'Bob', 'last_name': 'Johnson', 'password': 'password123'},
                {'username': 'maria_garcia', 'email': 'maria@example.com', 'first_name': 'Maria', 'last_name': 'Garcia', 'password': 'password123'},
                {'username': 'alex_wong', 'email': 'alex@example.com', 'first_name': 'Alex', 'last_name': 'Wong', 'password': 'password123'},
            ]
            
            for user_data in test_users:
                password = user_data.pop('password')
                user = User.objects.create(**user_data)
                user.set_password(password)
                user.save()
                
                # Create a passenger record for each user
                Passenger.objects.create(
                    user=user,
                    passenger_name=f"{user.first_name} {user.last_name}",
                    contact_number=f"+63{random.randint(9000000000, 9999999999)}",
                    address=f"{random.randint(1, 999)} Sample St., Example City",
                    email=user.email
                )
                
                print(f"Created user and passenger: {user.username}")
        
        # Create sample staff if they don't exist
        if not Staff.objects.exists():
            # Create a staff user
            staff_user, created = User.objects.get_or_create(
                username='staff_user',
                defaults={
                    'email': 'staff@example.com',
                    'first_name': 'Staff',
                    'last_name': 'User',
                    'is_staff': True
                }
            )
            
            if created:
                staff_user.set_password('staffpass123')
                staff_user.save()
            
            # Create staff record
            Staff.objects.create(
                user=staff_user,
                staff_name=f"{staff_user.first_name} {staff_user.last_name}",
                position="Ferry Operator",
                contact_number="+639123456789",
                email=staff_user.email
            )
            
            print("Created staff user")
        
        # Create sample reservations if they don't exist or less than 10
        if Reservation.objects.count() < 10:
            # Get schedules that allow reservations
            reservable_schedules = Schedule.objects.filter(reserve=True)[:20]
            all_passengers = Passenger.objects.all()
            
            # Create different status reservations
            status_options = ['PENDING', 'CONFIRMED', 'CANCELLED', 'COMPLETED']
            
            for i, schedule in enumerate(reservable_schedules):
                # Pick a passenger
                passenger = random.choice(all_passengers)
                
                # Create the reservation with different statuses
                status = status_options[i % len(status_options)]
                
                # For completed/cancelled reservations, use past dates
                if status in ['COMPLETED', 'CANCELLED']:
                    reservation_date = timezone.now() - datetime.timedelta(days=random.randint(1, 10))
                else:
                    reservation_date = timezone.now() - datetime.timedelta(hours=random.randint(1, 24))
                
                reservation = Reservation.objects.create(
                    schedule=schedule,
                    passenger=passenger,
                    date_of_reservation=reservation_date,
                    status=status
                )
                
                # Create payment for CONFIRMED and COMPLETED reservations
                if status in ['CONFIRMED', 'COMPLETED']:
                    # Random deposit amount (between 20% and 100% of the ticket price)
                    deposit_percentage = random.randint(20, 100)
                    deposit_amount = (schedule.price * deposit_percentage) / 100
                    
                    # Random payment method
                    payment_methods = ['CREDIT_CARD', 'DEBIT_CARD', 'GCASH', 'PAYMAYA', 'BANK_TRANSFER']
                    payment_method = random.choice(payment_methods)
                    
                    Payment.objects.create(
                        reservation=reservation,
                        amount=deposit_amount,
                        payment_date=reservation_date + datetime.timedelta(minutes=random.randint(5, 30)),
                        payment_method=payment_method,
                        payment_status='COMPLETED',
                        transaction_reference=f"RES-{uuid.uuid4().hex[:12].upper()}"
                    )
                
                print(f"Created reservation with status {status} for {passenger.passenger_name}")
        
        print("Sample data creation complete!")

# Create a function to ensure all schedules allow reservations for testing
def enable_all_reservations():
    """Enable reservations for all schedules to make testing easier"""
    schedules = Schedule.objects.all()
    count = schedules.update(reserve=True)
    print(f"Enabled reservations for {count} schedules")

# Create a function to reset reservation status
def reset_reservation_status(reservation_id):
    """Reset a specific reservation to PENDING status for testing"""
    try:
        reservation = Reservation.objects.get(pk=reservation_id)
        reservation.status = 'PENDING'
        reservation.save()
        print(f"Reset reservation #{reservation_id} to PENDING status")
    except Reservation.DoesNotExist:
        print(f"Reservation #{reservation_id} not found")

if __name__ == "__main__":
    # When run directly, create the sample data
    create_sample_data()
    enable_all_reservations()
