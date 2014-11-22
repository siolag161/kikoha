from django.conf.urls import url, include, patterns

from .views import LinkDetailView, LinkCreateView, LinkUpdateView, LinkListView, LinkAuthorListView

urlpatterns = patterns( 
    "",

    url(r'^(?P<pk>\d+)/?$', LinkDetailView.as_view(), name="detail"),
    url(r'^(?P<pk>\d+)/(?P<uslug>[-\w]+)/?$', LinkDetailView.as_view(), name="detail_slug"),

    url(r'^create/?', LinkCreateView.as_view(), name="create"),
    url(r'^list/?', LinkListView.as_view(), name="list"),
    url(r'^author/(?P<user_pk>\d+)/?$', LinkAuthorListView.as_view(), name="list_by_author"), # by author id


)
