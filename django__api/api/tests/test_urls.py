from django.test import SimpleTestCase
from django.urls import reverse, resolve
from api import views


class TestUrls(SimpleTestCase):

    def test_token_login_url_resolves(self):
        url = reverse('api:token_login')
        self.assertEquals(resolve(url).func, views.token_login)

    def test_search_events_url_resolves(self):
        url = reverse('api:search_events')
        self.assertEquals(resolve(url).func, views.search_ticketmaster_events)

    def test_save_event_url_resolves(self):
        url = reverse('api:save_event')
        self.assertEquals(resolve(url).func, views.update_saved_events)

    def test_delete_event_url_resolves(self):
        url = reverse('api:delete_event')
        self.assertEquals(resolve(url).func, views.delete_saved_event)

    def test_update_recommended_events_url_resolves(self):
        url = reverse('api:update_recommended_events')
        self.assertEquals(resolve(url).func, views.update_recommended_events)

    def test_render_recommended_events_url_resolves(self):
        url = reverse('api:render_recommended_events')
        self.assertEquals(resolve(url).func, views.render_recommended_events)

    def test_get_saved_events_url_resolves(self):
        url = reverse('api:get_saved_events')
        self.assertEquals(resolve(url).func, views.get_saved_events)

    def test_get_recommended_events_url_resolves(self):
        url = reverse('api:get_recommended_events')
        self.assertEquals(resolve(url).func, views.get_recommended_events)

    def test_get_ticketmaster_events_url_resolves(self):
        url = reverse('api:get_ticketmaster_events')
        self.assertEquals(resolve(url).func, views.get_ticketmaster_events)
