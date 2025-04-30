from django import forms
from .models import Reservation, Payment, Passenger
from django.core.validators import MinValueValidator
from django.utils import timezone
import datetime

class ReservationForm(forms.ModelForm):
    """Form for creating a reservation"""
    
    class Meta:
        model = Reservation
        fields = ['schedule']  # Include schedule field to ensure proper validation
    
    def __init__(self, *args, **kwargs):
        self.schedule = kwargs.pop('schedule', None)
        self.passenger = kwargs.pop('passenger', None)
        super().__init__(*args, **kwargs)
        
        # Set the schedule as a hidden field with the initial value
        if self.schedule:
            self.fields['schedule'].initial = self.schedule.pk
            self.fields['schedule'].widget = forms.HiddenInput()
            self.fields['schedule'].disabled = False
        
        # Add CSS classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Check if the schedule allows reservations
        if self.schedule and not self.schedule.reserve:
            raise forms.ValidationError("This schedule does not allow reservations.")
        
        # Check if schedule is in the past
        if self.schedule and self.schedule.departure_time < timezone.now():
            raise forms.ValidationError("Cannot reserve tickets for past schedules.")
        
        # Check if the departure is within 24 hours
        if self.schedule and self.schedule.departure_time - timezone.now() < datetime.timedelta(hours=24):
            raise forms.ValidationError("Reservations must be made at least 24 hours before departure.")
        
        return cleaned_data

class ReservationPaymentForm(forms.ModelForm):
    CARD_TYPE_CHOICES = [
        ('VISA', 'Visa'),
        ('MC', 'MasterCard'),
        ('AMEX', 'American Express'),
        ('JCB', 'JCB')
    ]
    
    # Custom payment method choices with Filipino options
    PAYMENT_METHOD_CHOICES = [
        ('CREDIT_CARD', 'Credit Card'),
        ('DEBIT_CARD', 'Debit Card'),
        ('GCASH', 'GCash'),
        ('PAYMAYA', 'Maya'),
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('7ELEVEN', '7-Eleven'),
    ]
    
    payment_method = forms.ChoiceField(choices=PAYMENT_METHOD_CHOICES)
    card_type = forms.ChoiceField(choices=CARD_TYPE_CHOICES, required=False)
    card_number = forms.CharField(max_length=19, required=False, 
                                  widget=forms.TextInput(attrs={'placeholder': 'XXXX-XXXX-XXXX-XXXX'}))
    expiry_date = forms.CharField(max_length=7, required=False, 
                                  widget=forms.TextInput(attrs={'placeholder': 'MM/YYYY'}))
    cvv = forms.CharField(max_length=4, required=False, 
                          widget=forms.TextInput(attrs={'placeholder': 'XXX'}))
    
    # For GCash/Maya
    mobile_number = forms.CharField(max_length=11, required=False,
                                  widget=forms.TextInput(attrs={'placeholder': '09XXXXXXXXX'}))
    
    # For Bank Transfer
    bank_name = forms.CharField(max_length=50, required=False)
    account_name = forms.CharField(max_length=100, required=False)
    reference_number = forms.CharField(max_length=20, required=False)
    
    # Reservation deposit amount (typically a percentage of the total ticket price)
    deposit_percentage = forms.IntegerField(
        initial=20,  # Default 20% deposit
        min_value=10,
        max_value=100,
        help_text="Percentage of the total ticket price to pay as deposit (minimum 10%)",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Payment
        fields = ['payment_method']
        
    def __init__(self, *args, **kwargs):
        self.reservation = kwargs.pop('reservation', None)
        self.schedule_price = kwargs.pop('schedule_price', 0)
        super().__init__(*args, **kwargs)
        
        # Add CSS classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
        # Make payment_method a select field with custom CSS
        self.fields['payment_method'].widget = forms.Select(
            choices=self.PAYMENT_METHOD_CHOICES,
            attrs={'class': 'form-select'}
        )
    
    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')
        deposit_percentage = cleaned_data.get('deposit_percentage', 20)
        
        if payment_method in ['CREDIT_CARD', 'DEBIT_CARD']:
            card_number = cleaned_data.get('card_number')
            expiry_date = cleaned_data.get('expiry_date')
            cvv = cleaned_data.get('cvv')
            
            if not card_number:
                self.add_error('card_number', 'Card number is required for card payments.')
            if not expiry_date:
                self.add_error('expiry_date', 'Expiry date is required for card payments.')
            if not cvv:
                self.add_error('cvv', 'CVV is required for card payments.')
        
        elif payment_method in ['GCASH', 'PAYMAYA']:
            mobile_number = cleaned_data.get('mobile_number')
            
            if not mobile_number:
                self.add_error('mobile_number', 'Mobile number is required for GCash/Maya payments.')
            elif not mobile_number.startswith('09') or len(mobile_number) != 11:
                self.add_error('mobile_number', 'Please enter a valid Philippine mobile number (e.g., 09XXXXXXXXX).')
        
        elif payment_method == 'BANK_TRANSFER':
            bank_name = cleaned_data.get('bank_name')
            reference_number = cleaned_data.get('reference_number')
            
            if not bank_name:
                self.add_error('bank_name', 'Bank name is required for bank transfers.')
            if not reference_number:
                self.add_error('reference_number', 'Reference number is required for bank transfers.')
        
        # Validate deposit percentage
        if deposit_percentage < 10:
            self.add_error('deposit_percentage', 'Minimum deposit is 10% of the ticket price.')
        elif deposit_percentage > 100:
            self.add_error('deposit_percentage', 'Maximum deposit cannot exceed 100% of the ticket price.')
        
        return cleaned_data
    
    def get_deposit_amount(self):
        """Calculate the deposit amount based on the percentage and schedule price"""
        deposit_percentage = self.cleaned_data.get('deposit_percentage', 20)
        return (self.schedule_price * deposit_percentage) / 100
