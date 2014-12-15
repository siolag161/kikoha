from django.conf.urls import url, include, patterns

from .views import CommunityCreateView, CommunityListView, community_detail

 
urlpatterns = patterns(
    "",
    url(r'^/?$', CommunityListView.as_view(), name="community_list"),
    url(r'^~create/?$', CommunityCreateView.as_view(), name="community_create"),
    url(r'^(?P<name>[-\w]+)/?$', community_detail, name="community_detail"),

)

