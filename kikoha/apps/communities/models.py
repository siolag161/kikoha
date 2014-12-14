from django.db.models import URLField, permalink, CharField, SlugField, ForeignKey
from django.utils.translation import ugettext_lazy as _

from core.models import BasePostModel, ScoredModel
from voting.models import VotedModel


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
 
"""
"""
class Link(BasePostModel, ScoredModel, VotedModel):
    url = URLField(null=False)
    community = ForeignKey(Community, verbose_name=_("Community"), related_name='links')

    @permalink
    def get_absolute_url(self):
	return 'community:link_detail', (), {'name': self.community.name, 'pk': self.id, 'uslug': self.slug}
    
    def save(self, *args, **kwargs):
	super(Link,self).save(*args,**kwargs)

    def __unicode__(self):
	return self.title
