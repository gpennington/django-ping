from django.conf.urls.defaults import patterns, url

from ping.views import status


urlpatterns = patterns(
    '',

    url(r'^$', status, name='status'),
)
