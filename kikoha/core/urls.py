from django.conf.urls import url, patterns

from .views import home, cached_home


urlpatterns = patterns(
    '',
    url(r'^$', cached_home, name='home'),
)
