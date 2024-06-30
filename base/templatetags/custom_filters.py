# myapp/templatetags/custom_filters.py
from django import template
from django.utils.timesince import timesince
from datetime import datetime

register = template.Library()

@register.filter
def timesince_simplified(value):
    if not isinstance(value, datetime):
        return value
    
    time_since = timesince(value)
    return time_since.split(',')[0]  # Return only the first part (e.g., "1 hour")
