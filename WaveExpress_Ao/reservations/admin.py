from django.contrib import admin
from .models import Destination, Schedule, Reservation

admin.site.register(Destination)
admin.site.register(Schedule)
admin.site.register(Reservation)
