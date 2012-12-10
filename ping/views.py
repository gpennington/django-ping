from django.http import HttpResponse
from django.conf import settings
from django.utils import simplejson

from ping import defaults

def status(request):
    """
    Returns a simple HttpResponse
    """
    
    response = getattr(settings, 'PING_DEFAULT_RESPONSE', defaults.PING_DEFAULT_RESPONSE)
    mimetype = getattr(settings, 'PING_DEFAULT_MIMETYPE', defaults.PING_DEFAULT_MIMETYPE)
    
    if request.GET.get('fmt') == 'json':
        response = simplejson.dumps({ 'up': True })
        mimetype = 'application/json'
        
    return HttpResponse(response, mimetype=mimetype, status=200)