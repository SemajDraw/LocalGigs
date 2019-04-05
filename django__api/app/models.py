from django.db import models
from django.contrib.postgres.fields.jsonb import JSONField
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.http import HttpRequest


# Profile table model, each column of the table is defined here, what data types it
# holds and what initial parameters and restrictions are put on it. This table is linked to
# the user table as a one to one relationship.
class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(
        max_length=2,
        choices=GENDER_CHOICES,
        blank=True,
    )
    profile_picture = models.ImageField(upload_to='media/user/profile_images',
                                        default='default_profile.jpeg')
    saved_events = JSONField(blank=True, null=True, default=list)
    recommended_events = JSONField(blank=True, null=True, default=list)

    # Display the email as the identifier in django admin (Profile)
    def __str__(self):
        return self.user.email


# Spotify table model, stores the users access token and details on their playlist contents
# Defines what initial parameters and restrictions are put on it the fields
# This table is linked to the user table as a one to one relationship.
class Spotify(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_data = JSONField(blank=True, null=True)
    artist_count = JSONField(blank=True, null=True)
    recommended_artists = JSONField(blank=True, null=True, default=list)

    # Display the email as the identifier in django admin (Spotify)
    def __str__(self):
        return self.user.email


# This is a trigger that is fired once a user is created,
# it creates a profile and spotify table entry for the new user
@receiver(post_save, sender=User)
def create_user_profiles(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Spotify.objects.create(user=instance)


# This is a trigger that is fired once a user is created,
# it saves the Users profile
@receiver(post_save, sender=User)
def save_user_profiles(sender, instance, **kwargs):
    instance.profile.save()
    instance.spotify.save()


# This is a trigger that is fired once a user is created,
# it creates an authentication token for the User that can be used
# to log in via the API.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

