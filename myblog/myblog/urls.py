from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from django.conf import settings
urlpatterns = patterns('',
     url(r'^', include('blg.urls')),
     url(r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.STATIC_ROOT,}),
     url(r'^admin/', include(admin.site.urls)),
     url(r'^captcha/', include('captcha.urls')),
)
