# coding: utf-8

from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver

from django.db import models

from core.models import OwnedModel, TimeStampedModel
from .managers import VoteManager

POINTS = (
    (+1, '+1'), 
    (-1, '-1'),
)

## todo: define maybe a contenttype base class
@python_2_unicode_compatible
class Vote(OwnedModel, TimeStampedModel, models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    object = generic.GenericForeignKey('content_type', 'object_id')
    vote = models.SmallIntegerField(choices = POINTS )

    objects = VoteManager()

    class Meta:
	db_table = 'votes'
	unique_together = (('author', 'content_type', 'object_id'),)
        
    def __str__(self):
        return '%s: %s on %s' % (self.author, self.vote, self.object)

    def is_upvote(self):
        return self.vote == 1

    def is_downvote(self):
        return self.vote == -1


UPDATE_TYPES = {
    'CLEARED': -1,
    'ADDED': +1,
    'CREATED': +1
}

class VotedModel(models.Model):
    upvotes = models.PositiveIntegerField(default=1)
    totalvotes = models.IntegerField(default=1)
    
    @property
    def downvotes(self):
	return totalvotes - upvotes

    @property
    def point(self):
	return 2*self.upvotes - self.totalvotes # upvotes - downvotes
    
    class Meta:
        abstract = True

    def get_point(self):
	return { 'point': self.point, 'num_votes': self.totalvotes }

    def update_vote(self, update_type, vote):
	if update_type and vote:
	    change = UPDATE_TYPES[update_type]
	    self.totalvotes += change
	    if vote.is_upvote():
		self.upvotes += change
	    self.save()
