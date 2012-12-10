from django.conf import settings
from django.utils.importlib import import_module

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
                func = getattr(mod, attr)
            except AttributeError:
                raise ImproperlyConfigured('Module "%s" does not define a "%s" callable' % (module, attr))
            
            key, value = func(request)
            response_dict[key] = value

    return response_dict
    
def check_database_sessions(request):
    from django.contrib.sessions.models import Session
    try:
        session = Session.objects.all()[0]
        return 'db_sessions', True
    except:
        return 'db_sessions', False

def check_database_sites(request):
    from django.contrib.sites.models import Site
    try:
        session = Site.objects.all()[0]
        return 'db_site', True
    except:
        return 'db_site', False
        
def check_cache_set(request):        
    from django.core.cache import cache
    try:
        cache.set('django-ping-test', 'abc123', 30)
        return 'cache_set', True
    except:
        return 'cache_set', False

def check_cache_get(request):        
    from django.core.cache import cache
    try:
        data = cache.get('django-ping-test')
        if data == 'abc123':
            return 'cache_get', True
        else:
            return 'cache_get', False
    except:
        return 'cache_get', False


