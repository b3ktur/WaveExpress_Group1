from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from ferry_system.models import Port, Ferry, Route, Schedule, Passenger
import datetime
import random

class Command(BaseCommand):
    help = 'Creates sample data for the ferry reservation system'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data for WaveExpress...')
        
        # Create ports if they don't exist
        if Port.objects.count() == 0:
            self.stdout.write('Creating ports...')
            ports = [
                {'port_name': 'Manila Pier', 'location': 'Manila'},
                {'port_name': 'Batangas Port', 'location': 'Batangas'},
                {'port_name': 'Calapan Port', 'location': 'Oriental Mindoro'},
                {'port_name': 'Cebu Port', 'location': 'Cebu City'},
                {'port_name': 'Tagbilaran Port', 'location': 'Bohol'},
                {'port_name': 'Dumaguete Port', 'location': 'Negros Oriental'},
            ]
            
            for port_data in ports:
                Port.objects.create(**port_data)
            
            self.stdout.write(self.style.SUCCESS(f'Created {len(ports)} ports'))
        else:
            self.stdout.write('Ports already exist, skipping creation')
        
        # Create ferries if they don't exist
        if Ferry.objects.count() == 0:
            self.stdout.write('Creating ferries...')
            ferries = [
                {'ferry_name': 'WaveRider 1', 'capacity': 150, 'model': 'Standard Passenger Ferry', 'registration_number': 'WR-001-2025'},
                {'ferry_name': 'WaveRider 2', 'capacity': 200, 'model': 'Premium Passenger Ferry', 'registration_number': 'WR-002-2025'},
                {'ferry_name': 'OceanStar', 'capacity': 300, 'model': 'Luxury Passenger Ferry', 'registration_number': 'OS-001-2025'},
                {'ferry_name': 'WaveRunner', 'capacity': 250, 'model': 'High-Speed Passenger Ferry', 'registration_number': 'WRU-001-2025'},
                {'ferry_name': 'Sea Eagle', 'capacity': 180, 'model': 'Standard Passenger Ferry', 'registration_number': 'SE-001-2025'},
            ]
            
            for ferry_data in ferries:
                Ferry.objects.create(**ferry_data)
            
            self.stdout.write(self.style.SUCCESS(f'Created {len(ferries)} ferries'))
        else:
            self.stdout.write('Ferries already exist, skipping creation')
        
        # Create routes if they don't exist
        if Route.objects.count() == 0:
            self.stdout.write('Creating routes...')
            
            # Get all ports
            ports = list(Port.objects.all())
            
            routes = []
            # Create routes between different ports
            for i in range(len(ports)):
                for j in range(i+1, len(ports)):
                    if i != j:
                        departure_port = ports[i]
                        arrival_port = ports[j]
                        
                        # Generate route name based on port names
                        route_name = f"{departure_port.port_name.split(' ')[0]} - {arrival_port.port_name.split(' ')[0]}"
                        
                        # Generate a random distance between 50 and 500 km
                        distance = round(random.uniform(50, 500), 2)
                        
                        # Create the route
                        Route.objects.create(
                            route_name=route_name,
                            departure_port=departure_port,
                            arrival_port=arrival_port,
                            distance=distance
                        )
                        
                        # Also create the reverse route
                        reverse_route_name = f"{arrival_port.port_name.split(' ')[0]} - {departure_port.port_name.split(' ')[0]}"
                        Route.objects.create(
                            route_name=reverse_route_name,
                            departure_port=arrival_port,
                            arrival_port=departure_port,
                            distance=distance
                        )
                        
                        routes.append(route_name)
                        routes.append(reverse_route_name)
            
            self.stdout.write(self.style.SUCCESS(f'Created {len(routes)} routes'))
        else:
            self.stdout.write('Routes already exist, skipping creation')
        
        # Create schedules for the next 14 days that allow reservations
        self.stdout.write('Creating schedules...')
        
        # Get all routes and ferries
        routes = Route.objects.all()
        ferries = Ferry.objects.all()
        
        # Delete any existing future schedules to avoid conflicts
        future_schedules = Schedule.objects.filter(departure_time__gte=timezone.now())
        deleted_count = future_schedules.count()
        future_schedules.delete()
        self.stdout.write(f'Deleted {deleted_count} future schedules')
        
        # Create new schedules
        schedule_count = 0
        
        # Start from tomorrow to ensure 24-hour reservation window
        start_date = timezone.now().date() + datetime.timedelta(days=1)
        end_date = start_date + datetime.timedelta(days=14)
        
        for route in routes:
            # Assign a random ferry to each route
            ferry = random.choice(ferries)
            
            # Create a schedule for each day
            current_date = start_date
            while current_date <= end_date:
                # Morning departure
                departure_time_am = timezone.make_aware(
                    datetime.datetime.combine(
                        current_date, 
                        datetime.time(hour=8, minute=0)
                    )
                )
                
                # Calculate arrival time (assume 1 hour per 50km)
                travel_hours = max(1, int(route.distance / 50))
                arrival_time_am = departure_time_am + datetime.timedelta(hours=travel_hours)
                
                # Set a price based on distance (₱500 base + ₱5 per km)
                price_am = 500 + (route.distance * 5)
                
                # Create morning schedule with reservation enabled
                Schedule.objects.create(
                    ferry=ferry,
                    route=route,
                    departure_time=departure_time_am,
                    arrival_time=arrival_time_am,
                    price=price_am,
                    reserve=True  # Enable reservations
                )
                schedule_count += 1
                
                # Afternoon departure
                departure_time_pm = timezone.make_aware(
                    datetime.datetime.combine(
                        current_date, 
                        datetime.time(hour=15, minute=0)
                    )
                )
                
                # Calculate arrival time (same logic)
                arrival_time_pm = departure_time_pm + datetime.timedelta(hours=travel_hours)
                
                # Set a price based on distance (slightly higher for afternoon)
                price_pm = 550 + (route.distance * 5)
                
                # Create afternoon schedule with reservation enabled
                Schedule.objects.create(
                    ferry=ferry,
                    route=route,
                    departure_time=departure_time_pm,
                    arrival_time=arrival_time_pm,
                    price=price_pm,
                    reserve=True  # Enable reservations
                )
                schedule_count += 1
                
                # Move to next day
                current_date += datetime.timedelta(days=1)
        
        self.stdout.write(self.style.SUCCESS(f'Created {schedule_count} new schedules'))
        
        # Create a test user if it doesn't exist
        if not User.objects.filter(username='testuser').exists():
            user = User.objects.create_user(
                username='testuser',
                email='testuser@example.com',
                password='testpassword',
                first_name='Test',
                last_name='User'
            )
            
            # Create passenger profile for the test user
            Passenger.objects.create(
                user=user,
                passenger_name='Test User',
                contact_number='09123456789',
                address='123 Test Street, Test City',
                email='testuser@example.com'
            )
            
            self.stdout.write(self.style.SUCCESS('Created test user: testuser (password: testpassword)'))
        
        self.stdout.write(self.style.SUCCESS('Sample data creation complete!'))
