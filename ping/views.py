from django.http import HttpResponse
from django.conf import settings
from django.utils import simplejson

from ping.defaults import *
from ping.checks import checks


def status(request):
    """
    Returns a simple HttpResponse
    """
    
    response = getattr(settings, 'PING_DEFAULT_RESPONSE', PING_DEFAULT_RESPONSE)
    mimetype = getattr(settings, 'PING_DEFAULT_MIMETYPE', PING_DEFAULT_MIMETYPE)
    
    if request.GET.get('fmt') == 'json':
        response_dict = checks(request)
        response = simplejson.dumps(response_dict)
        mimetype = 'application/json'  

    return HttpResponse(response, mimetype=mimetype, status=200)