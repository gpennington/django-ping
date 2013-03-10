from django.http import HttpResponse
from django.conf import settings
from django.utils import simplejson
from django.contrib.auth.decorators import login_required

from ping.defaults import *
from ping.checks import checks
from ping.decorators import http_basic_auth

@http_basic_auth
def status(request):
    """
    Returns a simple HttpResponse
    """
        
    response = "<h1>%s</h1>" % getattr(settings, 'PING_DEFAULT_RESPONSE', PING_DEFAULT_RESPONSE)
    mimetype = getattr(settings, 'PING_DEFAULT_MIMETYPE', PING_DEFAULT_MIMETYPE)
    
    if request.GET.get('checks') == 'true':
        response_dict = checks(request)
        response += "<dl>"
        for key, value in sorted(response_dict.items()):
            response += "<dt>%s</dt>" % str(key)
            response += "<dd>%s</dd>" % str(value)
        response += "</dl>"

    if request.GET.get('fmt') == 'json':
        try:
            response = simplejson.dumps(response_dict)
        except UnboundLocalError:
            response_dict = checks(request)
            response = simplejson.dumps(response_dict)
        response = simplejson.dumps(response_dict, sort_keys=True)
        mimetype = 'application/json'  

    return HttpResponse(response, mimetype=mimetype, status=200)