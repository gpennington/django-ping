PING_DEFAULT_RESPONSE = "Your site is up!"
PING_DEFAULT_MIMETYPE = 'text/html'

PING_DEFAULT_CHECKS = (
    'ping.checks.CheckDatabaseSessions',
    'ping.checks.CheckDatabaseSites',
    'ping.checks.CheckCacheSet',
    'ping.checks.CheckCacheGet',
)

PING_BASIC_AUTH = False

PING_CELERY_TIMEOUT = 5

PING_CACHE_KEY = 'django-ping-test'
PING_CACHE_VALUE = 'abc123'
