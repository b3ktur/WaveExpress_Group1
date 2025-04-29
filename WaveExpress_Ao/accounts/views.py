from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, ProfileUpdateForm
from .models import UserProfile
from ferry_system.models import Passenger, Staff

def landing_page(request):
    """Simple landing page view"""
    return render(request, 'landing.html')

def register_view(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create a user profile
            profile = UserProfile.objects.create(
                user=user,
                phone_number=form.cleaned_data.get('phone_number'),
                address=form.cleaned_data.get('address')
            )
            
            # Create a passenger record
            Passenger.objects.create(
                user=user,
                passenger_name=f"{user.first_name} {user.last_name}",
                contact_number=profile.phone_number or '',
                address=profile.address or '',
                email=user.email
            )
            
            # Log the user in
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    """User login view"""
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('landing')

@login_required
def profile_view(request):
    """User profile view"""
    try:
        # Check if user is a passenger
        passenger = Passenger.objects.get(user=request.user)
        is_passenger = True
    except Passenger.DoesNotExist:
        passenger = None
        is_passenger = False
    
    try:
        # Check if user is a staff member
        staff = Staff.objects.get(user=request.user)
        is_staff = True
    except Staff.DoesNotExist:
        staff = None
        is_staff = False
    
    context = {
        'passenger': passenger,
        'staff': staff,
        'is_passenger': is_passenger,
        'is_staff': is_staff
    }
    
    return render(request, 'accounts/profile.html', context)

@login_required
def profile_update(request):
    """Update user profile view"""
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            
            # Update passenger record if exists
            try:
                passenger = Passenger.objects.get(user=request.user)
                passenger.contact_number = form.cleaned_data.get('phone_number') or passenger.contact_number
                passenger.address = form.cleaned_data.get('address') or passenger.address
                passenger.save()
            except Passenger.DoesNotExist:
                pass
            
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'accounts/profile_update.html', {'form': form})

def home_view(request):
    """Home page view"""
    return render(request, 'home.html')
