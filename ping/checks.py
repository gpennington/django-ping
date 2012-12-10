from django.conf import settings
from django.utils.importlib import import_module

from ping.defaults import *

def checks():
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
            
            key, value = func()
            response_dict[key] = value

    return response_dict
    

def check_database_sessions():
    from django.contrib.sessions.models import Session
    try:
        session = Session.objects.all()[0]
        return 'db_sessions', True
    except:
        return 'db_sessions', False

def check_database_sites():
    from django.contrib.sites.models import Site
    try:
        session = Site.objects.all()[0]
        return 'db_site', True
    except:
        return 'db_site', False
