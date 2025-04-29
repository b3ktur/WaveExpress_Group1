# WaveExpress - Ferry Ticket Booking System

A simplified web application for booking ferry tickets across the Philippines.

## Project Features

1. **User Authentication**
   - Landing page with login form
   - User registration
   - Session management

2. **Ferry Booking System**
   - Search for available schedules by origin, destination, date, and passenger count
   - Book reservations
   - View reservation history
   - Check seat availability

3. **MySQL Stored Procedure**
   - Custom stored procedure for finding available schedules
   - Efficient schedule search with multiple criteria

## Setup Instructions

### Prerequisites
- Python 3.8+
- MySQL Server
- pip (Python package manager)

### Installation Steps

1. **Clone the repository**
   ```
   git clone <repository-url>
   cd WaveExpress_Group1_Ao
   ```

2. **Set up a virtual environment (optional but recommended)**
   ```
   python -m venv .venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```
     .venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source .venv/bin/activate
     ```

4. **Install required packages**
   ```
   pip install django mysqlclient
   ```

5. **Create the MySQL database**
   ```sql
   CREATE DATABASE dbwaveexpress_ao;
   ```

6. **Apply migrations**
   ```
   cd WaveExpress_Ao
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Import sample data**
   Open MySQL console and run:
   ```
   USE dbwaveexpress_ao;
   SOURCE sample_data.sql;
   ```

8. **Create a superuser**
   ```
   python manage.py createsuperuser
   ```

9. **Run the development server**
   ```
   python manage.py runserver
   ```

10. **Access the application**
    - Website: http://127.0.0.1:8000/
    - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

- **accounts**: Handles user authentication (login/register)
- **reservations**: Manages ferry schedules and bookings

## User Flow

1. User arrives at the landing page
2. User logs in or registers for a new account
3. User searches for available ferry schedules
4. User selects a schedule and books a reservation
5. User can view all their reservations

## Stored Procedure

The project uses a MySQL stored procedure `FindAvailableSchedules` to efficiently search for available schedules based on:
- Origin location
- Destination
- Travel date
- Number of passengers

This provides a more efficient way to query the database compared to standard ORM queries.
