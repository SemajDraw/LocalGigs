from django.test import TestCase
from django.contrib.auth.models import User
from app import models


# class TestModels(TestCase):

    # def setUp(self):
    #     self.user = User.objects.create()
    #     self.profile = models.Profile.objects.create(
    #         user=
    #         bio='',
    #         age=31,
    #         gender='M',
    #         saved_events=[],
    #         recommended_events=[]
    #     )
    #
    #     self.spotify = models.Spotify.objects.create(
    #         user_data={"data": "some user data"},
    #         artist_count={"Led Zeppelin": 20},
    #         recommended_artists=["Frank Zappa", "The Animals"]
    #     )
    #
    # def test_user_assigned_profile_spotify_on_create(self):
    #     self.assertEquals(models.Spotify)
    #     self.assertEquals(models.Profile)
