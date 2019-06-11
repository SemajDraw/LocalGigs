from django.test import SimpleTestCase
from django.urls import reverse, resolve
from app import views


class TestAppUrls(SimpleTestCase):

    def test_landing_url_resolved(self):
        url = reverse('app:landing')
        self.assertEquals(resolve(url).func, views.landing)

    def test_home_url_resolved(self):
        url = reverse('app:home')
        self.assertEquals(resolve(url).func, views.home)

    def test_profile_url_resolved(self):
        url = reverse('app:profile')
        self.assertEquals(resolve(url).func, views.profile)

    def test_update_profile_url_resolved(self):
        url = reverse('app:update_profile')
        self.assertEquals(resolve(url).func, views.update_profile)

    def test_update_profile_pic_url_resolved(self):
        url = reverse('app:update_profile_pic')
        self.assertEquals(resolve(url).func, views.update_profile_pic)


