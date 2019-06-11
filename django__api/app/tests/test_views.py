from django.test import TestCase
from django.urls import reverse


class TestViews(TestCase):

    def test_landing_view(self):
        response = self.client.get(reverse('app:landing'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/landing.html')

    def test_home_view(self):
        response = self.client.get(reverse('app:home'))
        self.assertRedirects(
            response,
            '/accounts/login/?next=/home/',
            status_code=302,
            fetch_redirect_response=False)

    def test_profile_view(self):
        response = self.client.get(reverse('app:profile'))
        self.assertRedirects(
            response,
            '/accounts/login/?next=/profile/',
            status_code=302,
            fetch_redirect_response=False)

    def test_update_profile_view(self):
        response = self.client.get(reverse('app:update_profile'))
        self.assertRedirects(
            response,
            '/accounts/login/?next=/update_profile_details/',
            status_code=302,
            fetch_redirect_response=False)

    def test_update_profile_pic_view_no_POST(self):
        response = self.client.get(reverse('app:update_profile_pic'))
        self.assertRedirects(
            response,
            '/accounts/login/?next=/profile/update_profile_pic/',
            status_code=302,
            fetch_redirect_response=False)

