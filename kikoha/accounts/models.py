# -*- coding: utf-8 -*-
# Import the AbstractUser model
from django.contrib.auth.models import AbstractUser

# Import the basic Django ORM models library
from django.db import models

from django.utils.translation import ugettext_lazy as _

class User(AbstractUser):
    """
    username
    first_name
    last_name
    
    link_karma
    comment_karma
    total_karma

    self_desc
    
    friends 
    ennemies
    """ 
 
    link_karma = models.IntegerField(_('link karma'), null=True, blank=True)
    comment_karma = models.IntegerField(_('comment karma'), null=True, blank=True)
    #total_karma = models.IntegerField()    
    desc = models.CharField(_('description'), max_length = 500, null=True, blank=True)

    @property
    def total_karmas(self, include_old = True):
	return None
	
    def __unicode__(self):
        return self.username
 
