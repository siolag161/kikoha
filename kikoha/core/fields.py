from __future__ import unicode_literals

from django.db.models.fields import SlugField
from .tools import slugify, get_sourced_value, crop_string


from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now

DEFAULT_CHOICES_NAME = 'STATUS'


class AutoCreatedField(models.DateTimeField):
    """
    A DateTimeField that automatically populates itself at
    object creation.
    By default, sets editable=False, default=timezone.now (fixes timezone)
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', False)
        kwargs.setdefault('default', now)
        super(AutoCreatedField, self).__init__(*args, **kwargs)

    def pre_save(self, instance, add):
	val = now()
	if add:
	    setattr(instance, self.attname, val)
	return val

class CoreSlugField(models.CharField):
    
    def __init__(self, *args, **kwargs):
	kwargs['max_length'] = kwargs.get('max_length', 250)
	self.source_from = kwargs.pop('source_from',None)
	#kwargs.setdefault('editable',False)
	kwargs['unique'] = False # never enforce uniqueness
	kwargs.setdefault('db_index',True)
	
	super(models.CharField,self).__init__(*args,**kwargs)

    def pre_save(self, instance, add):
	val = self.value_from_object(instance)
	if not val and self.source_from:
	    val = get_sourced_value(self.source_from,instance)
	if val:
	    val = slugify(val)
	else:
	    val = None	    
            if not self.blank:
		val = instance._meta.module_name
	    elif not self.null:
		val = ''
	if val and self.max_length:
	   val = crop_string(val, self.max_length)	

	setattr(instance, self.attname, val)
	return val

    
