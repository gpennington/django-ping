from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings


PING_CHECKS_FULL = (
    'ping.checks.check_database_sessions',
    'ping.checks.check_database_sites',
    'ping.checks.check_cache_set',
    'ping.checks.check_cache_set',
    'ping.checks.check_user_exists',
)

PING_CHECKS_BAD = (
    'pong.checks.check_database_sessions',
)

PING_CHECKS_BAD2 = (
    'ping.checks.check_foo',
)

class PingTest(TestCase):
    urls = 'ping.urls'    

    def setUp(self):
        self.client = Client()

    def test_endpoint(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)

    @override_settings(PING_CHECKS=PING_CHECKS_FULL)
    def test_checks(self):
        response = self.client.get("?checks=true")
        self.assertEqual(response.status_code, 200)

    def test_json(self):
        response = self.client.get("?fmt=json")
        self.assertEqual(response.status_code, 200)