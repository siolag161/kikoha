from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.db.models import Sum, Count
from django.contrib.contenttypes.models import ContentType

from signals import vote_recorded

import logging
logger = logging.getLogger("werkzeug")

ZERO_VOTES_ALLOWED = getattr(settings, 'VOTING_ZERO_VOTES_ALLOWED', False)

### todo:
"""
1. change score -> point (x)
2. cache the voting info in the object in-self
2.bis. update the model once finished
3. django signals
4. async task for updating the score
"""
class VoteManager(models.Manager):
    def get_point(self, obj):
        """
        Get a dictionary containing the total point for ``obj`` and
        the number of votes it's received.
        """
	result = {}

	get_obj_point = getattr(obj, 'get_point', None)
	if callable(get_obj_point):	
	    result = get_obj_point()
	else:
	    ctype = ContentType.objects.get_for_model(obj)
	    result = self.filter(
		object_id=obj._get_pk_val(),
		content_type=ctype
	    ).aggregate(
		point=Sum('vote'),
		num_votes=Count('vote')
	    )

	if result['point'] is None:
	    result['point'] = 0
	logger.info("point: " + str(result)) 
        return result

    def get_points_in_bulk(self, objects):
        """
        Get a dictionary mapping object ids to total point and number
        of votes for each object.
        """
        object_ids = [o._get_pk_val() for o in objects]
        if not object_ids:
            return {}

        ctype = ContentType.objects.get_for_model(objects[0])

        queryset = self.filter(
            object_id__in=object_ids,
            content_type=ctype,
        ).values(
            'object_id',
        ).annotate(
            point=Sum('vote'), 
            num_votes=Count('vote')
        )

        vote_dict = {}
        for row in queryset:
            vote_dict[row['object_id']] = {
                'point': int(row['point']),
                'num_votes': int(row['num_votes']),
            }

        return vote_dict

    def record_vote(self, obj, user, vote):
        """
        Record a user's vote on a given object. Only allows a given user
        to vote once, though that vote may be changed.
        A zero vote indicates that any existing vote should be removed.
        """
        if vote not in (+1, 0, -1):
            raise ValueError('Invalid vote (must be +1/0/-1)')
        ctype = ContentType.objects.get_for_model(obj)
        try:
            v = self.get(author=user, content_type=ctype,
                         object_id=obj._get_pk_val())
	    
            if vote == 0 and not ZERO_VOTES_ALLOWED:
		# vote = v.vote
                v.delete()
		update_type = 'CLEARED'
            else:
		v.vote = vote
                v.save()
		update_type = 'ADDED'
	    vote_recorded.send( sender=v.__class__, object = obj, vote=v, update_type=update_type )
	   
        except models.ObjectDoesNotExist:	    
            if not ZERO_VOTES_ALLOWED and vote == 0:
                return
            v = self.create(author=user, content_type=ctype,
                        object_id=obj._get_pk_val(), vote=vote)
	    update_type = 'CREATED'
	    # logger.info('created - sent by: %s - %s - %s' % (v, obj, update_type))
	    vote_recorded.send( sender=v.__class__, object = obj, vote=v, update_type=update_type )

	    # vote_recorded.send( sender=v, object=obj,
	    # 		                update_type=update_type )


    def get_top(self, model, limit=10, reversed=False):
        """
        Get the top N pointd objects for a given model.
        Yields (object, point) tuples.
        """
        ctype = ContentType.objects.get_for_model(model)
        results = self.filter(content_type=ctype).values('object_id').annotate(point=Sum('vote'))
        if reversed:
            results = results.order_by('point')
        else:
            results = results.order_by('-point')

        # Use in_bulk() to avoid O(limit) db hits.
        objects = model.objects.in_bulk([item['object_id'] for item in results[:limit]])

        # Yield each object, point pair. Because of the lazy nature of generic
        # relations, missing objects are silently ignored.
        for item in results[:limit]:
            id, point = item['object_id'], item['point']
            if not point:
                continue
            if id in objects:
                yield objects[id], int(point)

    def get_bottom(self, Model, limit=10):
        """
        Get the bottom (i.e. most negative) N pointd objects for a given
        model.
        Yields (object, point) tuples.
        """
        return self.get_top(Model, limit, True)

    def get_for_user(self, obj, user):
        """
        Get the vote made on the given object by the given user, or
        ``None`` if no matching vote exists.
        """
        if not user.is_authenticated():
            return None
        ctype = ContentType.objects.get_for_model(obj)
        try:
            vote = self.get(content_type=ctype, object_id=obj._get_pk_val(),
                            author=user)
        except models.ObjectDoesNotExist:
            vote = None
        return vote

    def get_for_user_in_bulk(self, objects, user):
        """
        Get a dictionary mapping object ids to votes made by the given
        user on the corresponding objects.
        """
        vote_dict = {}
        if len(objects) > 0:
            ctype = ContentType.objects.get_for_model(objects[0])
            votes = list(self.filter(content_type__pk=ctype.id,
                                     object_id__in=[obj._get_pk_val() \
                                                    for obj in objects],
                                     author__pk=user.id))
            vote_dict = dict([(vote.object_id, vote) for vote in votes])
        return vote_dict
