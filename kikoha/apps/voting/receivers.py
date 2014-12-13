from django.dispatch import receiver
from django.db.models.signals import post_save

from .signals import vote_recorded
from .models import Vote

import logging
logger = logging.getLogger("werkzeug")

#

'''
    upvotes = models.PositiveIntegerField(default=1)
    totalvotes = models.IntegerField(default=1)
'''

@receiver(vote_recorded, sender=Vote)
def update_vote_count(sender, **kwargs):
    # logger.info('received: %s' % sender )
    
    update_type = kwargs.get('update_type', None)
    vote = kwargs.get('vote', None)
    obj = kwargs.get('object', None)
    
    if update_type and vote and obj:
	# todo checks here if has callable
	obj.update_vote(update_type, vote)
    	# change = UPDATE_TYPES[update_type]
	# obj.totalvotes += change
	# if change == 1 and vote == 1:
	#     obj.upvotes += 1
	# elif change == -1 and vote == 1:
	#     obj.upvotes -= 1
	# obj.save()


# @receiver(post_save, sender=Vote)
# def update_vote_count(sender, **kwargs):
#     logger.info('received')

#     # update_type = kwargs.get('update_type', None)
#     # vote = kwargs.get('vote', None)
#     # obj = kwargs.get('object', None)

#     # if update_type and vote and obj:
#     # 	change = UPDATE_TYPES[update_type]
#     # 	obj.upvotes += change
#     # 	obj.totalvotes += change
#     # 	obj.save()
