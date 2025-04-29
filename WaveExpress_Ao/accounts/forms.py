from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        # Change username help text to more friendly message
        self.fields['username'].help_text = "Create a unique username. You'll use this to log in."
        # Make password help texts more user-friendly
        self.fields['password1'].help_text = "Your password must be at least 8 characters long and contain letters and numbers. Don't use common passwords."
        self.fields['password2'].help_text = "Enter the same password again to verify."

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username / Email')
    
    class Meta:
        model = User
        fields = ['username', 'password']
