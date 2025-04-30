from django import template
from django.utils import timezone
import datetime

register = template.Library()

@register.filter
def split(value, arg):
    """
    Splits a string by the given separator and returns the result as a list.
    Example: {{ value|split:" " }}
    """
    return value.split(arg)

@register.filter
def get_item(value, index):
    """
    Gets an item from a list by index.
    Example: {{ value|get_item:0 }}
    """
    try:
        index = int(index)
        return value[index]
    except (IndexError, TypeError, ValueError):
        return ''

@register.filter
def trim(value):
    """
    Trims leading and trailing whitespace.
    Example: {{ value|trim }}
    """
    if isinstance(value, str):
        return value.strip()
    return value

@register.filter
def time_since(value):
    """
    Returns the time remaining until 24 hours after the given datetime.
    """
    if not value:
        return "No deadline"
    
    now = timezone.now()
    deadline = value + datetime.timedelta(hours=24)
    
    if now > deadline:
        return "Expired"
    
    diff = deadline - now
    hours = diff.seconds // 3600
    minutes = (diff.seconds % 3600) // 60
    
    if diff.days > 0:
        return f"{diff.days}d {hours}h {minutes}m"
    elif hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"
