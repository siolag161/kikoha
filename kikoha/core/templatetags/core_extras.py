
from django.utils import timezone
from datetime import datetime, timedelta
from django import template
from django.utils.timesince import timesince

register = template.Library()

@register.filter
def minus(val, by):
    return val - by

@register.filter
def age(time):
    now = timezone.now()
    try:
	diff = now - time
    except:
	return time
    if diff <= timedelta(minutes=1):
	return 'just now'
    return '%(time)s ago' % {'time': timesince(time) }
