from django.conf import settings
from django.http import HttpResponse

def status(request):
    """
    Returns a simple HttpResponse
    """
    
    response = getattr(settings, 'PING_DEFAULT_RESPONSE', ping.defaults.PING_DEFAULT_RESPONSE)
    mimetype = getattr(settings, 'PING_DEFAULT_MIMETYPE', ping.defaults.PING_DEFAULT_MIMETYPE)
    
    if request.GET.get('json'):
        response = simplejson.dumps({ 'up': True })
        mimetype = 'application/json'
        
    return HttpResponse(response, mimetype=mimetype, status=200)