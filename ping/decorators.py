from functools import wraps

from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.conf import settings

from ping.defaults import PING_BASIC_AUTH


def http_basic_auth(func):
    """
    Attempts to login user with u/p provided in HTTP_AUTHORIZATION header.
    If successful, returns the view, otherwise returns a 401.
    If PING_BASIC_AUTH is False, then just return the view function

    Modified code by:
    http://djangosnippets.org/users/bthomas/
    from
    http://djangosnippets.org/snippets/1304/
    """
    @wraps(func)
    def _decorator(request, *args, **kwargs):
        if getattr(settings, 'PING_BASIC_AUTH', PING_BASIC_AUTH):
            if 'HTTP_AUTHORIZATION' in request.META:
                authmeth, auth = request.META['HTTP_AUTHORIZATION'].split(' ', 1)
                if authmeth.lower() == 'basic':
                    auth = auth.strip().decode('base64')
                    username, password = auth.split(':', 1)
                    user = authenticate(username=username, password=password)
                    if user:
                        login(request, user)
                        return func(request, *args, **kwargs)
                    else:
                        return HttpResponse("Invalid Credentials", status=401)
            else:
                return HttpResponse("No Credentials Provided", status=401)
        else:
            return func(request, *args, **kwargs)
    return _decorator
