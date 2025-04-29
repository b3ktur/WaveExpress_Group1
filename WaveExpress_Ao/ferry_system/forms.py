from django import forms
from .models import (
    Ferry, Port, Route, Schedule, Passenger, Ticket, 
    Reservation, Payment, Staff, FerryAssignment
)

# Forms will be implemented when needed for the templates
# These are just basic ModelForms to get started

class FerryForm(forms.ModelForm):
    class Meta:
        model = Ferry
        fields = ['ferry_name', 'capacity', 'model', 'registration_number']
        
class PortForm(forms.ModelForm):
    class Meta:
        model = Port
        fields = ['port_name', 'location']
        
class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['route_name', 'departure_port', 'arrival_port', 'distance']
        
class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['ferry', 'route', 'departure_time', 'arrival_time', 'price', 'reserve']
        widgets = {
            'departure_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'arrival_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['passenger_name', 'contact_number', 'address', 'email']
        
class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['schedule', 'passenger', 'seat_number']
        
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['schedule', 'passenger']
        
class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['staff_name', 'position', 'contact_number', 'email']
        
class FerryAssignmentForm(forms.ModelForm):
    class Meta:
        model = FerryAssignment
        fields = ['ferry', 'schedule', 'staff']
