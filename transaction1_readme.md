# Transaction #1: Passenger Buys a Ticket

This branch implements the first transaction for the WaveExpress Ferry System: allowing a passenger to browse schedules and purchase a ticket for ferry travel in the Philippines.

## Feature Overview

1. **Browse Schedules**: Users can view all available ferry schedules with filtering options by departure port, arrival port, and departure date across the Philippine archipelago.

2. **Purchase Ticket**: Authenticated users can select a schedule and purchase a ticket.

3. **Payment Processing**: Multiple Filipino payment methods including credit/debit cards, GCash, Maya, bank transfers, and more.

4. **Ticket Management**: Users can view their purchased tickets, see ticket details, and print tickets.

## Implementation Details

### Models Used
- `Schedule`: Displays available ferry schedules
- `Ticket`: Stores information about purchased tickets
- `Payment`: Handles payment information with Filipino payment options
- `Passenger`: Links tickets to user accounts

### Views
- `schedule_list`: Displays all available schedules with filtering options
- `buy_ticket`: Handles ticket purchase for a specific schedule
- `pay_ticket`: Processes payment for a purchased ticket
- `ticket_confirmation`: Shows confirmation after successful purchase
- `ticket_detail`: Displays detailed information about a purchased ticket
- `my_tickets`: Lists all tickets purchased by the current user
- `print_ticket`: Provides a printable version of a ticket
- `cancel_ticket`: Handles ticket cancellation (when allowed)

### Templates
- `schedule_list.html`: Lists all available schedules in the Philippines
- `buy_ticket.html`: Form for purchasing a ticket
- `payment.html`: Payment form with Filipino payment methods
- `confirmation.html`: Confirmation page after successful purchase
- `detail.html`: Detailed view of a specific ticket
- `my_tickets.html`: Lists all of a user's tickets
- `print_ticket.html`: Printable ticket view

### Forms
- `TicketPurchaseForm`: Form for capturing ticket information
- `TicketPaymentForm`: Form for processing payment with Filipino payment options

## Philippines-Specific Features

1. **Philippine Ports**: Added major Philippine ports including Cebu, Manila, Tagbilaran (Bohol), Batangas, and more.

2. **Local Routes**: Implemented popular ferry routes in the Philippines:
   - Cebu City to Tagbilaran (Bohol)
   - Manila to Batangas
   - Cebu City to Manila
   - And more

3. **Filipino Payment Options**:
   - Credit/Debit Cards
   - GCash
   - Maya (formerly PayMaya)
   - Bank Transfer (BDO, BPI, etc.)
   - Cash at Terminal
   - 7-Eleven
   - GrabPay
   - Coins.ph

4. **Pricing in Philippine Peso (₱)**: All ticket prices are displayed in Philippine Pesos.

## User Flow

1. User navigates to the Schedules page
2. User selects a schedule and clicks "Buy Ticket"
3. User fills out ticket information (seat preference)
4. User proceeds to payment
5. User completes payment using Filipino payment methods
6. User receives confirmation of ticket purchase
7. User can view, print, or cancel the ticket from the My Tickets page

## Testing Instructions

1. Make sure you've migrated the database:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

2. Run the server:
   ```
   python manage.py runserver
   ```

3. Create a user account or use the test account:
   - Username: `testuser`
   - Password: `password123`

4. Navigate to the Schedules page and test the transaction flow:
   - Try filtering schedules between Philippine ports
   - Purchase a ticket
   - Complete payment using Filipino payment methods
   - View ticket details
   - Print ticket
   - Try canceling a ticket
   
## Sample Data

The system includes sample data with:
- Popular Philippine ferry routes
- Filipino passenger names
- Realistic pricing for local routes
- Typical sailing durations between Philippine islands

## Screenshots

Screenshots of key pages can be added here when they become available in the actual deployed system.
