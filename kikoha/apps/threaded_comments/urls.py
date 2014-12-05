from django.conf.urls import url, include, patterns
from django.conf.urls import url, include

from .views import post_comment_ajax

urlpatterns = patterns (
     "",
    url(r'^post/ajax/$', post_comment_ajax, name='post-comment-ajax'),
    # url(r'^post/$', post_comment, name="comment_form"),
 )

