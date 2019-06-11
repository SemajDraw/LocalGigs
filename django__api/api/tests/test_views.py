from django.test import TestCase
from django.urls import reverse
import json


class TestViews(TestCase):

    # def setUp(self):
    #     self.event = {'save_event': '[{"date": {"day": "04", "month": "Nov"}, "name": "Greta Van Fleet", "time": "19:00:00", "image": "https://s1.ticketm.net/dam/a/fa5/d936214a-f378-492f-a502-ba4133d20fa5_869791_TABLET_LANDSCAPE_3_2.jpg", "venue": {"city": "Dublin", "name": "Olympia Theatre", "address": {"line1": "73 Dame Street"}, "country": "Ireland", "latitude": "53.344318", "longitude": "-6.266114", "venue_url": "https://www.ticketmaster.ie/Olympia-Theatre-tickets-Dublin/venue/198239"}, "spotify_url": "https://open.spotify.com/search/results/Greta%20Van%20Fleet", "youtube_url": "https://www.youtube.com/", "ticketmaster_url": "https://www.ticketmaster.ie/greta-van-fleet-dublin-11-04-2019/event/1800554AECDC89FB"}]'}

    def test_search_ticketmaster_events(self):
        response = self.client.get(reverse('api:search_events'))
        self.assertRedirects(
            response,
            '/accounts/login/?next=/api/search_events/',
            status_code=302,
            fetch_redirect_response=False)

    def test_render_recommended_events(self):
        response = self.client.get(reverse('api:render_recommended_events'))
        self.assertRedirects(
            response,
            '/accounts/login/?next=/api/render_recommended_events/',
            status_code=302,
            fetch_redirect_response=False)

    def test_get_saved_events(self):
        response = self.client.get(reverse('api:get_saved_events'))
        self.assertEquals(response.status_code, 200)


    # def test_update_saved_events(self):
    #     response = self.client.post(
    #         reverse('api:save_event'),
    #         data={'save_event': '[{"date": {"day": "04", "month": "Nov"}, "name": "Greta Van Fleet", "time": "19:00:00", "image": "https://s1.ticketm.net/dam/a/fa5/d936214a-f378-492f-a502-ba4133d20fa5_869791_TABLET_LANDSCAPE_3_2.jpg", "venue": {"city": "Dublin", "name": "Olympia Theatre", "address": {"line1": "73 Dame Street"}, "country": "Ireland", "latitude": "53.344318", "longitude": "-6.266114", "venue_url": "https://www.ticketmaster.ie/Olympia-Theatre-tickets-Dublin/venue/198239"}, "spotify_url": "https://open.spotify.com/search/results/Greta%20Van%20Fleet", "youtube_url": "https://www.youtube.com/", "ticketmaster_url": "https://www.ticketmaster.ie/greta-van-fleet-dublin-11-04-2019/event/1800554AECDC89FB"}]'})
    #     self.assertEquals(response.status_code, 200)


