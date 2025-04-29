from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserLoginForm
from .models import UserProfile

def landing_page(request):
    """Landing page view with login form"""
    if request.user.is_authenticated:
        return redirect('schedule_search')
        
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('schedule_search')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/landing.html', {'form': form})

def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('schedule_search')
        
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        
        if form.is_valid():
            # Create user
            user = form.save()
            
            # Create user profile
            UserProfile.objects.create(user=user)
            
            # Add success message
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}! You can now log in.")
            
            # Log the user in directly
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                messages.info(request, "You've been automatically logged in.")
                return redirect('schedule_search')
            else:
                return redirect('landing')
    else:
        form = UserRegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    """Logout view"""
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('landing')
