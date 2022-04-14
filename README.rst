Django Ping
===========

Django Ping is utility that provides a lightweight endpoint for availability and uptime monitoring services. It 
also provides hooks for testing stack components and reporting them via JSON.

Current Version: 0.3.0
https://github.com/gpennington/django-ping

Installation
------------

Use pip to download and install::

    pip install django-ping

Add Django Ping to url conf::

        url(r'^ping/', include('ping.urls')),

Basic Configuration
-------------------

Hitting the endpoint returns a simple status 200 response.
You can customize the message by adding to your Django settings::

    PING_DEFAULT_RESPONSE = "All systems go!"
    PING_DEFAULT_MIMETYPE = 'text/html'

Hitting the url::

    /ping
    
displays::

    All systems go!

Advanced Configuration
----------------------

Enable Status Checks
~~~~~~~~~~~~~~~~~~~~

Adding a ``checks=true`` parameter to the url tells Django Ping to run
a series of status checks and reports the results.

For example::

    /ping?checks=true
    
displays::

    Your site is up!
    db_sessions True
    db_site True

By default, Django Ping tests that your Database is responding
by using supplying two tests.  You can supply your own tests
to make sure everything is responding as expected. If you don't
use database sessions or the contrib.sites app, you can
remove the ones you don't need.

To customize, include a tuple in your Django settings::

    PING_CHECKS = (
        'ping.checks.check_database_sessions',
        #'ping.checks.check_database_sites',
        'my_app.module.check_function',
        'my_other_app.some_module.some_function'
    )


Specifying a ``fmt`` parameter to ``json`` returns more detailed and serialized data.
For example::

    /ping?fmt=json
    
displays::

    {
        "db_sessions": true,
        "db_site": true
    }

Custom Status Checks
~~~~~~~~~~~~~~~~~~~~

Checks should accept the request object and return
two values. The name/key to be displayed
and the value of the check. The value should be anything
that can be serialized.::

    def check_sample(request):
        #...do some things...
        return 'foo', True
        #or
        return 'bar', float(123.456)
        #or even
        return 'baz', ['one', 'two', 'three', {'a':1, 'b':2, 'c':3}]

Then, add that to the ``PING_CHECKS`` tuple to display::

    {
        'foo', true
    }

You can send ``POST`` requests too. As an example::

    def check_create_user(request):
        from django.contrib.auth.models import User
        try:
            if request.method == 'POST':
                username = request.GET.get('username')
                u, created = User.objects.get_or_create(username=username)
                if created:
                    return 'create_user', "User: %s has been created" % u.username
                else:
                    return 'create_user', "User: %s already exists" % u.username
            else:
                return 'create_user', "User cannot be created with GET"
        except:
            return 'create_user', "User not created"


Included Status Checks
~~~~~~~~~~~~~~~~~~~~~~

Django Ping includes a few checks to test various components
live.

**check_database_sessions** - Hits your database and attempts to retrieve a single session.

**check_database_sites** - Hits your database and attempts to retrieve a single site instance.

**check_cache_set** - Attempts to cache a value using the current cache backend defined.

**check_cache_get** - Attempts to retrieve a cached value using the current cache backend defined.

**check_celery** - Adds a task to the queue and checks for celery to complete it.


Authentication
~~~~~~~~~~~~~~

You can require HTTP Basic authentication to access the ping endpoint,
set ``PING_BASIC_AUTH`` to ``True`` in your Django settings.

Provide in the request the username/password of a valid User.

Complete Settings List
~~~~~~~~~~~~~~~~~~~~~~~~~

Check ``ping.defaults`` for default values.

PING_RESPONSE = "Some string"
PING_MIMETYPE = 'text/html' or valid content type
PING_DEFAULT_CHECKS  = tuple of paths to check methods
PING_BASIC_AUTH = Boolean (default is False)
PING_CELERY_TIMEOUT = In seconds as integers (5 is default) 


What's Next?
------------

Go sign up for a monitoring service or role your own.

https://www.pingdom.com/

http://www.panopta.com/

http://binarycanary.com/
