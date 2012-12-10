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
    

"""
Sample check method

Checks accept the request object and return
two values. The name of the key/node to be displayed
and the value of the check. The value should be anything
that can be serialized.

def check_sample():
    #...do some things...
    return 'foo', True
    #or
    return 'bar', ['one', 'two', 'three', {'a':1, 'b':2, 'c':3}]
"""

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
