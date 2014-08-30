try: # django.conf.urls.defaults was removed in django 1.6
  from django.conf.urls.defaults import patterns, include, url
except:
  from django.conf.urls import patterns, include, url
 
from ping.views import status

urlpatterns = patterns('',
    url(r'^$', status, name='status'),
)

