
def slugify(input, trans = None, obj = None, with_attr = None):
    from unidecode import unidecode
    from django.template import defaultfilters
    '''
    slugify a unicode string
    '''	
    return defaultfilters.slugify(unidecode(input))


def get_sourced_value(att, instance):
    if hasattr(att, '__call__'):
        return att(instance)
    else:
	attr_val = getattr(instance, att)
	return callable(attr_val) and attr_val() or attr_val


def crop_string(val, max_len):
    """ always ensures the len of val < max_len"""
    return val[:max_len]

    
	
    
def microsecs_since_midnight(date):
    """
    """
    from datetime import datetime
    mid_night = date.replace(hour=0, minute=0, second=0, microsecond=0)
    delta = date - mid_night
    return int(delta.total_seconds()*1000)
