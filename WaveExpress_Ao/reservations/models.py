from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

class Destination(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name

class Schedule(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.IntegerField(default=50)
    
    def is_available(self):
        return self.available_seats > 0
    
    def is_fully_booked(self):
        return self.available_seats == 0
    
    def is_almost_full(self):
        return self.available_seats <= 5
    
    def __str__(self):
        return f"{self.origin} to {self.destination.name} - {self.departure_date} {self.departure_time}"
    
    class Meta:
        ordering = ['departure_date', 'departure_time']

class Reservation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='reservations')
    number_of_passengers = models.IntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmed')
    booking_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.user.username} - {self.schedule}"
    
    def save(self, *args, **kwargs):
        # For new reservations only (not updates)
        if not self.pk:
            # Calculate the total price if not set
            if not self.total_price:
                # Base price without service fee
                self.total_price = self.schedule.price * self.number_of_passengers
            
            # Only update seats for confirmed reservations
            if self.status == 'confirmed':
                # Check if enough seats are available
                if self.schedule.available_seats < self.number_of_passengers:
                    raise ValueError("Not enough seats available for this schedule")
                
                # Update available seats
                self.schedule.available_seats -= self.number_of_passengers
                self.schedule.save()
        
        super(Reservation, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ['-booking_date']
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'
