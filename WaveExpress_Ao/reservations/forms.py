from django import forms
from .models import Reservation, Schedule

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['number_of_passengers']
        labels = {
            'number_of_passengers': 'Number of Passengers',
        }
        widgets = {
            'number_of_passengers': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }

class ScheduleSearchForm(forms.Form):
    origin = forms.CharField(required=True)
    destination = forms.CharField(required=True)
    departure_date = forms.DateField(widget=DateInput(), required=True)
    passengers = forms.IntegerField(min_value=1, max_value=10, initial=1)
