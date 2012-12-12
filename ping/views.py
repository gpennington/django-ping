from django.http import HttpResponse
from django.conf import settings
from django.utils import simplejson

from ping.defaults import *
from ping.checks import checks


def status(request):
    """
    Returns a simple HttpResponse
    """
    
    response = "<h1>%s</h1>" % getattr(settings, 'PING_DEFAULT_RESPONSE', PING_DEFAULT_RESPONSE)
    mimetype = getattr(settings, 'PING_DEFAULT_MIMETYPE', PING_DEFAULT_MIMETYPE)
    
    if request.GET.get('checks') == 'true':
        response_dict = checks(request)
        response += "<dl>"
        for key, value in response_dict.items():
            response += "<dt>%s</dt>" % str(key)
            response += "<dd>%s</dd>" % str(value)
        response += "</dl>"

    if request.GET.get('fmt') == 'json':
        response = simplejson.dumps(response_dict)
        mimetype = 'application/json'  

    return HttpResponse(response, mimetype=mimetype, status=200)