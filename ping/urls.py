from django.conf.urls.defaults import patterns, include, url
from ping.views import status

urlpatterns = patterns('',
    url(r'^$', status, name='status'),
)

