from django.conf import settings
from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured

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

#DEFAULT SYSTEM CHECKS

#Database    
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


#Caching
CACHE_KEY = 'django-ping-test'
CACHE_VALUE = 'abc123'

def check_cache_set(request):        
    from django.core.cache import cache
    try:
        cache.set(CACHE_KEY, CACHE_VALUE, 30)
        return 'cache_set', True
    except:
        return 'cache_set', False

def check_cache_get(request):        
    from django.core.cache import cache
    try:
        data = cache.get(CACHE_KEY)
        if data == CACHE_VALUE:
            return 'cache_get', True
        else:
            return 'cache_get', False
    except:
        return 'cache_get', False


#User
def check_user_exists(request):        
    from django.contrib.auth.models import User
    try:
        username = request.GET.get('username')
        u = User.objects.get(username=username)
        return 'user_exists', True
    except:
        return 'user_exists', False


#Celery
def check_celery(request):
    from datetime import datetime, timedelta
    from time import sleep
    from ping.tasks import sample_task

    now = datetime.now()
    expires = now + timedelta(seconds=getattr(settings, 'PING_CELERY_TIMEOUT', PING_CELERY_TIMEOUT))

    try:
        task = sample_task.apply_async(expires=expires)
        while expires > datetime.now():
            if task.ready() and task.result == True:
                return 'celery', True
            sleep(0.2)
        return 'celery', False
    except Exception, e:
        print e
        return 'celery', False
