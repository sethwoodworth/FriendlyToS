from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.http import HttpResponse

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('userena.urls')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: ", mimetype="text/plain")),
    url(r'^$', 'frndlyts.tosview.views.home', name='home'),
    url(r'^frndlyts/', include('frndlyts.tosview.urls')),
)
