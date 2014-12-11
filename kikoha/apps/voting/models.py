# coding: utf-8

from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from django.db import models

from core.models import OwnedModel, TimeStampedModel
from .managers import VoteManager

SCORES = (
    (+1, '+1'),
    (-1, '-1'),
)

## todo: define maybe a contenttype base class
@python_2_unicode_compatible
class Vote(OwnedModel, TimeStampedModel, models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    object = generic.GenericForeignKey('content_type', 'object_id')
    vote = models.SmallIntegerField(choices = SCORES )

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
