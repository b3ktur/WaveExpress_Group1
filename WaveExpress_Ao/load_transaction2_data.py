"""
Script to load sample data for Transaction #2: A passenger reserves a ticket
"""
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WaveExpress_Ao.settings')
django.setup()

# Import the sample data creation function
from ferry_system.transaction2_sample_data import create_sample_data, enable_all_reservations

if __name__ == "__main__":
    print("Loading sample data for Transaction #2: A passenger reserves a ticket")
    create_sample_data()
    enable_all_reservations()
    print("Sample data loading complete!")
