from django.shortcuts import render
from django.utils import timezone
from .models import Schedule, Port
import datetime

def schedule_list(request):
    """View to display available schedules"""
    ports = Port.objects.all().order_by('port_name')
    
    # Get filter parameters from request
    departure_port = request.GET.get('departure_port')
    arrival_port = request.GET.get('arrival_port')
    departure_date = request.GET.get('departure_date')
    
    # Start with all schedules in the future
    schedules = Schedule.objects.filter(
        departure_time__gt=timezone.now()
    ).order_by('departure_time')
    
    # Apply filters if provided
    if departure_port:
        schedules = schedules.filter(route__departure_port_id=departure_port)
    
    if arrival_port:
        schedules = schedules.filter(route__arrival_port_id=arrival_port)
    
    if departure_date:
        try:
            date_obj = datetime.datetime.strptime(departure_date, '%Y-%m-%d').date()
            schedules = schedules.filter(
                departure_time__year=date_obj.year,
                departure_time__month=date_obj.month,
                departure_time__day=date_obj.day
            )
        except ValueError:
            # Invalid date format, ignore this filter
            pass
    
    context = {
        'schedules': schedules,
        'ports': ports,
    }
    
    return render(request, 'ferry_system/schedule_list.html', context)
