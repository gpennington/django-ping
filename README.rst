Django Ping
===========

Django Ping is utility that provides a lightweight endpoint for availability and uptime monitoring services. It 
also provides hooks for testing stack components and reporting them via JSON or XML.

Installation
------------

Use pip to download and install::

    pip install django-ping

Add Django Ping to url conf::

        url(r'^ping/', include('ping.urls')),

Configuration and Use
---------------------

Basic
~~~~~

Hitting the endpoint returns a simple status 200 response.
You can customize the message by adding to your Django settings::

    PING_DEFAULT_RESPONSE = "Your site is up!"
    PING_DEFAULT_MIMETYPE = 'text/html'

Hitting the url::

    /ping
    
displays::

    Your site is up!

Advanced
~~~~~~~~

Specifying a ``fmt`` paramter returns more detailed and serialized data.
For example::

    /ping?fmt=json
    
displays::

    {
        "db_sessions": true,
        "db_site": true
    }

By default, Django Ping tests that your Database is responding
by using supplying two tests.  You can supply your own tests
to make sure everything is responding as expected. If you don't
use database sessions or the contrib.sites app, you can removed
remove the ones you don't need.

To customize, include a tuple in your Django settings::

    PING_CHECKS = (
        'ping.checks.check_database_sessions',
        #'ping.checks.check_database_sites',
        'my_app.module.check_function',
        'my_other_app.some_module.some_function'
    )

Custom Status Checks
~~~~~~~~~~~~~~~~~~~~

Checks should accept the request object and return
two values. The name of the key/node to be displayed
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
or:

    <foo>True</foo>

Docs
----

Check out the full documentation.

...soon...