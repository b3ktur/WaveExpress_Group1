from django.db import models
from django.contrib.auth.models import User

# This will now act as a link between Django Users and our Passenger/Staff models
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_staff_member = models.BooleanField(default=False)
    is_passenger = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
