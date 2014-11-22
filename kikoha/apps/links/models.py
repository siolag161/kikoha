from django.db.models import URLField, permalink

from core.models import BasePostModel

################################## CONCRETE CLASESSES #########################################
class Link(BasePostModel):
    url = URLField(null=False)

    @permalink
    def get_absolute_url(self):
	return 'links:detail_slug', (), {'pk': self.id, 'uslug': self.slug}
    
    def save(self, *args, **kwargs):
	super(Link,self).save(*args,**kwargs)

