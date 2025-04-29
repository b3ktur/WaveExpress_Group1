from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError


class Ferry(models.Model):
    ferry_id = models.AutoField(primary_key=True)
    ferry_name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    model = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.ferry_name} ({self.registration_number})"
    
    class Meta:
        verbose_name_plural = "Ferries"


class Port(models.Model):
    port_id = models.AutoField(primary_key=True)
    port_name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.port_name} - {self.location}"


class Route(models.Model):
    route_id = models.AutoField(primary_key=True)
    route_name = models.CharField(max_length=100)
    departure_port = models.ForeignKey(Port, on_delete=models.CASCADE, related_name='departure_routes')
    arrival_port = models.ForeignKey(Port, on_delete=models.CASCADE, related_name='arrival_routes')
    distance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.route_name}: {self.departure_port.port_name} to {self.arrival_port.port_name}"
    
    def clean(self):
        if self.departure_port == self.arrival_port:
            raise ValidationError("Departure and arrival ports cannot be the same.")


class Schedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    ferry = models.ForeignKey(Ferry, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    reserve = models.BooleanField(default=False)  # Added as requested

    def __str__(self):
        return f"{self.route.route_name} - {self.departure_time.strftime('%Y-%m-%d %H:%M')}"
    
    def clean(self):
        if self.departure_time >= self.arrival_time:
            raise ValidationError("Departure time must be before arrival time.")
        
        # Check for scheduling conflicts with the same ferry
        conflicts = Schedule.objects.filter(
            ferry=self.ferry,
            departure_time__lt=self.arrival_time,
            arrival_time__gt=self.departure_time
        ).exclude(pk=self.pk)
        
        if conflicts.exists():
            raise ValidationError("This ferry is already scheduled during this time period.")


class Passenger(models.Model):
    passenger_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    passenger_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    address = models.TextField()
    email = models.EmailField()

    def __str__(self):
        return f"{self.passenger_name} ({self.email})"


class Ticket(models.Model):
    TICKET_STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('USED', 'Used'),
        ('CANCELLED', 'Cancelled')
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('UNPAID', 'Unpaid'),
        ('PAID', 'Paid'),
        ('REFUNDED', 'Refunded')
    ]
    
    ticket_id = models.AutoField(primary_key=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(default=timezone.now)
    seat_number = models.CharField(max_length=10, blank=True, null=True)
    ticket_status = models.CharField(max_length=20, choices=TICKET_STATUS_CHOICES, default='ACTIVE')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='UNPAID')

    def __str__(self):
        return f"Ticket #{self.ticket_id} - {self.passenger.passenger_name}"


class Reservation(models.Model):
    RESERVATION_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled')
    ]
    
    reservation_id = models.AutoField(primary_key=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    date_of_reservation = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=RESERVATION_STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"Reservation #{self.reservation_id} - {self.passenger.passenger_name}"

    def clean(self):
        if not self.schedule.reserve:
            raise ValidationError("This schedule does not allow reservations.")


class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded')
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('CREDIT_CARD', 'Credit Card'),
        ('DEBIT_CARD', 'Debit Card'),
        ('GCASH', 'GCash'),
        ('PAYMAYA', 'Maya'),
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('CASH', 'Cash at Terminal'),
        ('7ELEVEN', '7-Eleven'),
        ('GRABPAY', 'GrabPay'),
        ('COINS_PH', 'Coins.ph')
    ]
    
    payment_id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    transaction_reference = models.CharField(max_length=100, blank=True, null=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=True, blank=True)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.ticket:
            return f"Payment for Ticket #{self.ticket.ticket_id}"
        elif self.reservation:
            return f"Payment for Reservation #{self.reservation.reservation_id}"
        else:
            return f"Payment #{self.payment_id}"

    def clean(self):
        if self.ticket is None and self.reservation is None:
            raise ValidationError("Payment must be associated with either a ticket or a reservation.")
        if self.ticket is not None and self.reservation is not None:
            raise ValidationError("Payment cannot be associated with both a ticket and a reservation.")


class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f"{self.staff_name} - {self.position}"
    
    class Meta:
        verbose_name_plural = "Staff"


class FerryAssignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    ferry = models.ForeignKey(Ferry, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    assignment_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Ferry {self.ferry.ferry_name} assigned to {self.schedule}"

    def clean(self):
        # Check if ferry is already assigned to another schedule at the same time
        conflicts = FerryAssignment.objects.filter(
            ferry=self.ferry,
            schedule__departure_time__lt=self.schedule.arrival_time,
            schedule__arrival_time__gt=self.schedule.departure_time
        ).exclude(pk=self.pk)
        
        if conflicts.exists():
            raise ValidationError("This ferry is already assigned to another schedule during this time period.")
