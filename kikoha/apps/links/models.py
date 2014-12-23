from django.db.models import URLField, permalink, CharField, SlugField, ForeignKey
from django.utils.translation import ugettext_lazy as _

from core.models import BasePostModel, ScoredModel
from communities.models import Community
from voting.models import VotedModel 

# Create your models here.
 
"""
"""
class Link(BasePostModel, ScoredModel, VotedModel):
    url = URLField(null=False)
    community = ForeignKey(Community, verbose_name=_("Community"), related_name='links')

    @permalink
    def get_absolute_url(self):
	return 'link:link_detail', (), {'name': self.community.name, 'pk': self.id, 'uslug': self.slug}
    
    def save(self, *args, **kwargs):
	super(Link,self).save(*args,**kwargs)

    def __unicode__(self):
	return self.title
