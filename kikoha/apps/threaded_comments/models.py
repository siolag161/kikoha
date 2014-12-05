from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from extensions.treebeard.mp_tree import MP_Node, MP_NodeManager

from .managers import CommentManager
from django.contrib.comments.models import Comment


class ThreadedComment(MP_Node, Comment):
    objects = CommentManager()

    #def save(self, *args, **kwargs):	
#	parent = kwargs.pop('parent', None)
	##if not parent:
	 #   ThreadedComment.add_root(**kwargs)
	#return super(ThreadedComment, self).save(*args, **kwargs)

    class Meta:
	#abstract = True
	db_table = "threaded_comments"
