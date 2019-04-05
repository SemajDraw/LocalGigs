from django.test import SimpleTestCase
from django.urls import reverse, resolve


class TestUrls(SimpleTestCase):

    def test_landing_url_resolved(self):
        assert 1 == 2
