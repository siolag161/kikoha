from django.db.models import URLField, permalink, CharField, SlugField, ForeignKey
from django.utils.translation import ugettext_lazy as _

from core.models import BasePostModel


################################## CONCRETE CLASESSES #########################################
"""
"""
class Community(BasePostModel):
    def __unicode__(self):
	return self.title
    
    @property
    def name(self):
	return self.title
	
    @permalink
    def get_absolute_url(self):
	return 'community:community_detail', (), {'name': self.title}

    class Meta:
	verbose_name_plural = 'Communities'
