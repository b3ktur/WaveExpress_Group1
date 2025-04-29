import os
import django
import datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WaveExpress_Ao.settings')
django.setup()

from django.contrib.auth.models import User
from reservations.models import Destination, Schedule, Reservation

def add_sample_data():
    # Create sample destinations
    destinations = [
        {
            'name': 'Boracay',
            'description': 'Famous for its pristine white sand beaches and crystal-clear waters.'
        },
        {
            'name': 'Palawan',
            'description': 'Known for its limestone cliffs, lagoons, and beautiful beaches.'
        },
        {
            'name': 'Cebu',
            'description': 'A vibrant city with historical landmarks and beautiful islands.'
        },
        {
            'name': 'Bohol',
            'description': 'Home to the Chocolate Hills and tarsiers.'
        },
        {
            'name': 'Siargao',
            'description': 'Known as the surfing capital of the Philippines.'
        }
    ]
    
    for dest_data in destinations:
        Destination.objects.get_or_create(
            name=dest_data['name'],
            defaults={
                'description': dest_data['description']
            }
        )
    
    # Get all destinations
    boracay = Destination.objects.get(name='Boracay')
    palawan = Destination.objects.get(name='Palawan')
    cebu = Destination.objects.get(name='Cebu')
    bohol = Destination.objects.get(name='Bohol')
    siargao = Destination.objects.get(name='Siargao')
    
    # Create schedules for the next 7 days
    today = datetime.date.today()
    origins = {
        'Manila': [boracay, palawan, siargao],
        'Cebu': [bohol, boracay],
        'Batangas': [cebu, palawan]
    }
    
    # Create sample schedules
    for days_offset in range(7):
        schedule_date = today + datetime.timedelta(days=days_offset)
        
        for origin, destinations in origins.items():
            for destination in destinations:
                # Morning schedule
                Schedule.objects.get_or_create(
                    origin=origin,
                    destination=destination,
                    departure_date=schedule_date,
                    departure_time=datetime.time(8, 0),  # 8:00 AM
                    defaults={
                        'price': 1500.00 if destination == boracay else 1200.00 if destination == palawan else 800.00,
                        'available_seats': 50
                    }
                )
                
                # Afternoon schedule
                Schedule.objects.get_or_create(
                    origin=origin,
                    destination=destination,
                    departure_date=schedule_date,
                    departure_time=datetime.time(15, 0),  # 3:00 PM
                    defaults={
                        'price': 1500.00 if destination == boracay else 1200.00 if destination == palawan else 800.00,
                        'available_seats': 50
                    }
                )
    
    print("Sample data has been successfully added to the database.")

if __name__ == "__main__":
    add_sample_data()
