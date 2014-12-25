from django.conf.urls import url, include, patterns

from .models import Link
from .views import LinkDetailView, LinkCreateView, LinkUpdateView, LinkListView, LinkAuthorListView

# todo: refactor the url to voting
from voting.views import vote_on_object

urlpatterns = patterns(
    "",
    url(r'^(?P<name>[-\w]+)/~create/?$', LinkCreateView.as_view(), name="link_create"),
    url(r'^(?P<name>[-\w]+)/(?P<pk>\d+)/(?P<uslug>[-\w]+)/?$', LinkDetailView.as_view(), name="link_detail"),
    url(r'^(?P<pk>\d+)/(?P<uslug>[-\w]+)/?$', LinkDetailView.as_view(), name="link_detail_slug"),
)

link_dict = {
    'model': Link,
    'template_object_name': 'link',
    'allow_xmlhttprequest': True,
}

urlpatterns += patterns('',
    url(r'^~vote/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/?$',
	vote_on_object, link_dict, name="link-voting"),
)
