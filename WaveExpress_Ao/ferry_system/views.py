from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import (
    Ferry, Port, Route, Schedule, Passenger, Ticket, 
    Reservation, Payment, Staff, FerryAssignment
)

# Import specific transaction views
from .ticket_views import *

# Main views will be implemented here
# For now, we're implementing specific transaction views in separate files
