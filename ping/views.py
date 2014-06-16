import json

from django.http import HttpResponse
from django.conf import settings
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt

from ping.defaults import PING_DEFAULT_RESPONSE, PING_DEFAULT_MIMETYPE
from ping.checks import checks
from ping.decorators import http_basic_auth


@csrf_exempt
@http_basic_auth
def status(request):
    """
    Returns a simple HttpResponse
    """

    response = "<h1>%s</h1>" % getattr(settings, 'PING_DEFAULT_RESPONSE', PING_DEFAULT_RESPONSE)
    content_type = getattr(settings, 'PING_DEFAULT_CONTENT_TYPE', PING_DEFAULT_CONTENT_TYPE)

    if request.GET.get('checks') == 'true':
        response_dict = checks(request)
        response += "<dl>"
        for key, value in sorted(response_dict.items()):
            response += "<dt>%s</dt>" % str(key)
            response += "<dd>%s</dd>" % str(value)
        response += "</dl>"

    if request.GET.get('fmt') == 'json':
        try:
            response = json.dumps(response_dict)
        except UnboundLocalError:
            response_dict = checks(request)
            response = simplejson.dumps(response_dict)
        response = simplejson.dumps(response_dict, sort_keys=True)
        content_type = 'application/json'

    return HttpResponse(response, content_type=content_type, status=200)
