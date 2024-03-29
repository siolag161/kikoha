
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from django.views.generic.base import RedirectView, TemplateView

from communities.views import CommunityListView
urlpatterns = [ 

    url(r'^/?$', CommunityListView.as_view(), name="home"), 
    # Core
    url(r'^', include('core.urls', namespace='core')),

    url(r'^users/', include("accounts.urls", namespace="users")),
    url(r'^accounts/', include('allauth.urls')), 
    url(r'^avatar/', include('avatar.urls')),

    # Root-level redirects for common browser requests
    url(r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'img/compressed/favicon.ico'), name='favicon.ico'),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots.txt'),

    # Admin URLs
    url(r'^admin/rq/', include('extensions.django_rq.urls')),
    url(r'^admin/rq/scheduler/', include('extensions.rq_scheduler.urls', namespace='rq_scheduler')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

]

admin.site.site_header = '%s Headquarters' % settings.PROJECT_NAME
admin.site.index_title = 'Base of Operations'

urlpatterns += [
    url(r'^c/', include("communities.urls", namespace="community") ),
    url(r'^c/', include("links.urls", namespace="link") ),

    url(r'^comments/', include('threaded_comments.urls', namespace="comments")),
    url(r'^comments/', include('django.contrib.comments.urls')),

]


if settings.DEBUG:
    urlpatterns += [
        # Testing 404 and 500 error pages
        url(r'^404/$', TemplateView.as_view(template_name='404.html'), name='404'),
        url(r'^500/$', TemplateView.as_view(template_name='500.html'), name='500'),
    ]

    try:
        from django.conf.urls.static import static
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

        import debug_toolbar
        urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]

    # Should only occur when debug mode is on for production testing
    except ImportError as e:
        import logging
        l = logging.getLogger(__name__)
        l.warning(e)
