from django.db import models
from django.contrib.postgres.fields.jsonb import JSONField
from django.contrib.gis.db import models as geo_models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


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
    last_location = geo_models.PointField(
        verbose_name="last known location",
        blank=True,
        null=True
    )
    profile_picture = models.ImageField(upload_to='media/user/profile_images',
                                        default='default_profile.jpeg')
    interested_html = models.TextField(blank=True)
    facebook_data = JSONField(blank=True, null=True)

    # Display the username as the identifier in django admin profile
    def __str__(self):
        return self.user.username


# This is a trigger that is fired once a user is created,
# it creates a profile table entry for the user
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# This is a trigger that is fired once a user is created,
# it saves the Users profile
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# This is a trigger that is fired once a user is created,
# it creates an authentication token for the User that can be used
# to log in via the API.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


