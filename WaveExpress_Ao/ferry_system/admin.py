from django.contrib import admin
from .models import Ferry, Port, Route, Schedule, Passenger, Ticket, Reservation, Payment, Staff, FerryAssignment

admin.site.register(Ferry)
admin.site.register(Port)
admin.site.register(Route)
admin.site.register(Schedule)
admin.site.register(Passenger)
admin.site.register(Ticket)
admin.site.register(Reservation)
admin.site.register(Payment)
admin.site.register(Staff)
admin.site.register(FerryAssignment)
