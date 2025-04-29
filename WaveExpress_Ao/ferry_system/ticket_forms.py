from django import forms
from .models import Ticket, Payment, Passenger
from django.core.validators import MinValueValidator

class TicketPurchaseForm(forms.ModelForm):
    seat_number = forms.CharField(
        required=False,
        max_length=10,
        help_text="Optional. If left blank, a seat will be assigned automatically."
    )
    
    class Meta:
        model = Ticket
        fields = ['seat_number']
    
    def __init__(self, *args, **kwargs):
        self.schedule = kwargs.pop('schedule', None)
        self.passenger = kwargs.pop('passenger', None)
        super().__init__(*args, **kwargs)
        
        # Add CSS classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_seat_number(self):
        seat_number = self.cleaned_data.get('seat_number')
        if seat_number:
            # Check if seat number is already taken for this schedule
            if Ticket.objects.filter(
                schedule=self.schedule,
                seat_number=seat_number,
                ticket_status='ACTIVE'
            ).exists():
                raise forms.ValidationError(f"Seat {seat_number} is already taken. Please choose another seat.")
        return seat_number

class TicketPaymentForm(forms.ModelForm):
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
        ('CASH', 'Cash at Terminal'),
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
    
    class Meta:
        model = Payment
        fields = ['payment_method']
        
    def __init__(self, *args, **kwargs):
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
        
        return cleaned_data
