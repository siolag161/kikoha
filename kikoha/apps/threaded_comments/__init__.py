"""
Change the attributes you want to customize
"""

from .models import ThreadedComment
from .forms import CommentForm

def get_model():
    return ThreadedComment

def get_form():
    return CommentForm
