# WaveExpress Ferry System

A web-based ferry ticket booking and management system developed with Django.

## Project Overview

WaveExpress is a comprehensive ferry management system that allows:
- Passengers to book tickets and make reservations
- Staff to manage ferries, schedules, and assignments
- Admin to oversee the entire system

## Features

1. **Passenger Features**
   - Buy tickets
   - Reserve tickets
   - Cancel reservations
   - Make payments

2. **Staff Features**
   - Assign ferries to schedules
   - Manage routes and ports
   
3. **Admin Features**
   - Manage all system components
   - View reports and analytics

## Database Schema

The system uses the following entities:
- **Ferry**: Stores information about available ferries
- **Port**: Information about ports
- **Route**: Routes between ports
- **Schedule**: Ferry schedules with times and prices
- **Passenger**: Passenger information
- **Ticket**: Ticket details
- **Reservation**: Reservation information
- **Payment**: Payment processing
- **Staff**: Staff information
- **FerryAssignment**: Assignment of ferries to schedules by staff

## Installation

1. Clone the repository
   ```
   git clone https://github.com/yourusername/WaveExpress_Group1_Ao.git
   cd WaveExpress_Group1_Ao
   ```

2. Create a virtual environment
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Configure database in settings.py

5. Apply migrations
   ```
   cd WaveExpress_Ao
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Load sample data (optional)
   ```
   python manage.py shell < ferry_system/sample_data.py
   ```
   
   Alternatively, you can use the batch file:
   ```
   load_ferry_data.bat
   ```

7. Create a superuser
   ```
   python manage.py createsuperuser
   ```

8. Run the development server
   ```
   python manage.py runserver
   ```

## Technologies Used

- **Backend**: Django
- **Database**: MySQL
- **Frontend**: HTML, CSS, Bootstrap
- **JavaScript**: For interactive elements

## Development Status

This project is currently under development.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributors

- Your Team Members
