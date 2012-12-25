PING_DEFAULT_RESPONSE = "Your site is up!"
PING_DEFAULT_MIMETYPE = 'text/html'

PING_DEFAULT_CHECKS = (
    'ping.checks.check_database_sessions',
    'ping.checks.check_database_sites',
)

PING_BASIC_AUTH = False

PING_CELERY_TIMEOUT = 5 