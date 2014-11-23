from django.conf.urls import url, include, patterns

from .views import LinkDetailView, LinkCreateView, LinkUpdateView, LinkListView, LinkAuthorListView, \
    CommunityCreateView, CommunityByNameDetailView

urlpatterns = patterns( 
    "",

    #url(r'^(?P<pk>\d+)/?$', LinkDetailView.as_view(), name="link_detail"),
    #url(r'^(?P<pk>\d+)/(?P<uslug>[-\w]+)/?$', LinkDetailView.as_view(), name="link_detail_slug"),
    url(r'^/l/create/?', LinkCreateView.as_view(), name="link_create"),
    #url(r'^list/?', LinkListView.as_view(), name="link_list"),
    
    #url(r'^author/(?P<user_pk>\d+)/?$', LinkAuthorListView.as_view(), name="link_list_by_author"), # by author id
    #url(r'^author/(?P<username>[-\w]+)/?$', LinkAuthorListView.as_view(), name="link_list_by_author_username"), # by author id
)

 
urlpatterns += patterns( 
    "",
    url(r'^~create/?', CommunityCreateView.as_view(), name="community_create"),
    #url(r'^(?P<pk>\d+)/?$', CommunityDetailView.as_view(), name="community_detail"),
    url(r'^(?P<name>[-\w]+)/?', CommunityByNameDetailView.as_view(), name="community_detail"),

)

