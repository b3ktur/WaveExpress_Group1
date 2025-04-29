# Transaction #2: A Passenger Reserves a Ticket

This document describes the implementation of Transaction #2 for the WaveExpress Ferry System, which allows passengers to reserve tickets for ferry trips.

## Overview

The reservation system allows passengers to reserve tickets by paying a deposit amount instead of the full ticket price upfront. Reservations can be later converted to completed status when the passenger is ready to travel. This feature provides flexibility for passengers who want to secure their seats in advance without paying the full amount immediately.

## Implementation Features

1. **Reservation Creation**: Passengers can reserve tickets for schedules that have the `reserve` flag set to `True`.
2. **Deposit Payment**: When making a reservation, passengers pay a deposit amount (minimum 10% of the ticket price).
3. **Reservation Management**: Passengers can view, manage, and cancel their reservations.
4. **Reservation Completion**: Reservations can be marked as completed when the passenger is ready to travel.
5. **Cancellation Policy**: Reservations can be cancelled with a full refund up to 48 hours before departure.

## Database Structure

The system uses the following models for the reservation system:

1. **Reservation Model**:
   - Reference to a Schedule
   - Reference to a Passenger
   - Reservation date
   - Status (PENDING, CONFIRMED, CANCELLED, COMPLETED)

2. **Payment Model**:
   - Reference to a Reservation
   - Amount
   - Payment date
   - Payment method
   - Payment status
   - Transaction reference

## Files Created/Modified

### New Files:

1. **`reservation_forms.py`**: Contains form classes for reservation creation and payment.
   - `ReservationForm`: For creating a new reservation
   - `ReservationPaymentForm`: For processing deposit payments

2. **`reservation_views.py`**: Contains view functions for reservation-related actions:
   - `reserve_ticket`: Creates a new reservation
   - `pay_reservation`: Processes deposit payment
   - `reservation_confirmation`: Shows confirmation after payment
   - `reservation_detail`: Displays reservation details
   - `my_reservations`: Lists all reservations for the current user
   - `cancel_reservation`: Handles reservation cancellation
   - `convert_to_ticket`: Marks a reservation as completed

3. **`transaction2_sample_data.py`**: Script to create sample data for testing.

4. **Templates**:
   - `reservation/reserve_ticket.html`: Form to create a reservation
   - `reservation/payment.html`: Form to pay the deposit
   - `reservation/confirmation.html`: Confirmation after successful payment
   - `reservation/detail.html`: Display reservation details
   - `reservation/my_reservations.html`: List of user's reservations

### Modified Files:

1. **`urls.py`**: Added URL patterns for the new reservation views.
2. **`models.py`**: Added "COMPLETED" status to Reservation model.
3. **`views.py`**: Created a simplified schedule listing view.
4. **`base.html`**: Added navigation link for "My Reservations".
5. **`schedule_list.html`**: Modified to show only reservation buttons.

## URL Patterns

The following URL patterns were added to handle reservation functionality:

- `/reservations/reserve/<int:schedule_id>/`: Create a new reservation
- `/reservations/pay/<int:reservation_id>/`: Pay the deposit for a reservation
- `/reservations/confirmation/<int:reservation_id>/`: Show confirmation after payment
- `/reservations/detail/<int:reservation_id>/`: View reservation details
- `/reservations/cancel/<int:reservation_id>/`: Cancel a reservation
- `/reservations/convert/<int:reservation_id>/`: Mark a reservation as completed
- `/reservations/my-reservations/`: View all reservations for the current user

## Business Rules

1. Only schedules with the `reserve` flag set to `True` can be reserved.
2. Reservations must be made at least 24 hours before departure.
3. A minimum deposit of 10% of the ticket price is required to confirm a reservation.
4. Reservations can be cancelled up to 48 hours before departure for a full refund.
5. Reserved tickets must be converted to completed status to finalize the reservation.

## User Interface Flow

1. User browses available schedules and clicks "Reserve" on a schedule that allows reservations.
2. User confirms the reservation details and agrees to the terms.
3. User pays the deposit amount to confirm the reservation.
4. User receives confirmation of the reservation.
5. User can later mark the reservation as completed when ready to travel.
6. User can cancel the reservation up to 48 hours before departure.

## Security Measures

1. All reservation views require user authentication.
2. Access to reservation details and actions is restricted to the owner of the reservation.
3. Validation checks ensure that only valid reservations can be made and modified.
4. Appropriate status checks prevent invalid operations on reservations.

## Testing

To test the reservation functionality:

1. Run the `transaction2_sample_data.py` script to create sample data.
2. Log in as one of the sample users (e.g., username: john_doe, password: password123).
3. Browse available schedules and attempt to reserve a ticket.
4. Test the deposit payment process with different payment methods.
5. Verify that reservations appear in the "My Reservations" list.
6. Test the completion of a reservation.
7. Test the cancellation of a reservation.

## Sample Data

The `transaction2_sample_data.py` script creates the following sample data:

1. 5 ferry boats with different capacities
2. 10 ports in various locations in the Philippines
3. Routes between all combinations of ports
4. Schedules for the next 30 days
5. 5 test users with passenger profiles
6. 1 staff user
7. 10 sample reservations with different statuses
8. Payments for confirmed reservations

To run the sample data script:
```python
python manage.py shell
from ferry_system.transaction2_sample_data import create_sample_data
create_sample_data()
```

## Note for Developers

When implementing future transactions that interact with the reservation system, consider:

1. The different status states of a reservation (PENDING, CONFIRMED, CANCELLED, COMPLETED).
2. The payment tracking for deposits.
3. The validation checks for timing restrictions (24-hour/48-hour rules).
