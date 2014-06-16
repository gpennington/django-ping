from django.conf.urls import patterns, url

from ping.views import status


urlpatterns = patterns(
    '',

    url(r'^$', status, name='status'),
)
