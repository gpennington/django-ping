import inspect
from time import time

from django.conf import settings
from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured

#Check requirements
from django.core.cache import cache
from django.contrib.sites.models import Site
from django.contrib.sessions.models import Session

from ping.defaults import *

def checks(request):
    """
    Iterates through a tuple of systems checks,
    then returns a key name for the check and the value
    for that check.
    """
    response_dict = {}
    
    #Taken straight from Django
    #If there is a better way, I don't know it
    for path in getattr(settings, 'PING_CHECKS', PING_DEFAULT_CHECKS):
            i = path.rfind('.')
            module, attr = path[:i], path[i+1:]
            try:
                mod = import_module(module)
            except ImportError as e:
                raise ImproperlyConfigured('Error importing module %s: "%s"' % (module, e))
            try:
                check = getattr(mod, attr)
            except AttributeError:
                raise ImproperlyConfigured('Module "%s" does not define a "%s" callable' % (module, attr))
            

            #If check is a class, create instance of it and call
            #the _check method
            #Otherwise, just call the check directly
            if inspect.isclass(check):
                instance = check(request)
                response_dict.update(instance._check(request))
            else:
                check(request)
            
    return response_dict


class Check(object):

    def __init__(self, request):
        pass
    
    def _check(self, request):
        if hasattr(self, 'key'):
            response = {}
            start = time()
            
            response[self.key] = self.check(request)

            finished = str(time() - start)
            response[self.key]['time'] = finished
            return response
        else:
            raise AttributeError("Class %s must define a 'key' value" % self.__class__.__name__)
        
    def check(self, request):
        return {}


#DEFAULT SYSTEM CHECKS
#Database
class CheckDatabaseSessions(Check):
    key = 'db_sessions'
    def check(self, request):
        try:
            session = Session.objects.all()[0]
            return {'success': True}
        except:
            return {'success': False}

class CheckDatabaseSites(Check):
    key = 'db_sites'
    def check(self, request):
        try:
            session = Site.objects.all()[0]
            return {'success':True}
        except:
            return {'success': False}

#Caching
class CheckCacheSet(Check):
    key = 'cache_set'
    def check(self, request):
        try:
            cache.set(getattr(settings, 'PING_CACHE_KEY', PING_CACHE_KEY), getattr(settings, 'PING_CACHE_VALUE', PING_CACHE_VALUE), 30)
            return {'success':True}
        except:
            return {'success': False}

class CheckCacheGet(Check):
    key = 'cache_get'
    def check(self, request):
        try:
            data = cache.get(getattr(settings, 'PING_CACHE_KEY', PING_CACHE_KEY))
            if data == getattr(settings, 'PING_CACHE_VALUE', PING_CACHE_VALUE):
                return {'success':True}
            else:
                return {'success':False}
        except:
            return {'success': False}
