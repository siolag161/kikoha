from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from model_utils.models import StatusModel
from model_utils.fields import AutoLastModifiedField

from core import tools
from .fields import CoreSlugField, AutoCreatedField


user_model_label = getattr(settings, "AUTH_USER_MODEL", "auth.User")
try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
    get_user_model = lambda: User

class ScoredModel(models.Model):
    """
    Index this one
    """
    score = models.FloatField(default=0.0)
    class Meta:
        abstract = True

class OwnedModel(models.Model): 
    """ 
    """
    author = models.ForeignKey(user_model_label, verbose_name=_("Author"), related_name="%(class)ss")

    class Meta:
	abstract = True
    
class SluggedModel(models.Model):
    """
    An abstract class for class with a slug
    """
    title = models.CharField(_('Title'), max_length=255)
    slug = CoreSlugField(_('Slug'), source_from = "title", null=True, blank=True)    
    class Meta:
	abstract = True
	
class TimeStampedModel(models.Model):
    created = AutoCreatedField(_('created'))
    modified = AutoLastModifiedField(_('modified'))

    class Meta:
        abstract = True

class TimeFramedModel(models.Model):
    start = models.DateTimeField(_('start'), null=True, blank=True)
    end = models.DateTimeField(_('end'), null=True, blank=True)

    class Meta:
        abstract = True
	
class BasePostModel(OwnedModel, SluggedModel, TimeStampedModel, TimeFramedModel):
    """
    Base abstract model for a Post
    """    
    class Meta:
	abstract = True

    

