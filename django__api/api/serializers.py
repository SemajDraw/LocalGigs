from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists, get_username_max_length
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_gis import serializers as geo_serializers
from app.models import Profile, Spotify


# Data serialization for the Profile table
class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('bio', 'age', 'saved_events', 'recommended_events')

    def update(self, instance, validated_data):
        instance.bio = validated_data.get('bio', instance.bio)
        instance.age = validated_data.get('age', instance.age)
        instance.saved_events = validated_data.get('saved_events', instance.saved_events)
        instance.recommended_events = validated_data.get('recommended_events', instance.recommended_events)
        instance.save()
        return instance


# Data serialization for the Spotify table
class SpotifySerializer(serializers.ModelSerializer):

    class Meta:
        model = Spotify
        fields = ('user_data', 'artist_count', 'recommended_artists')

    def update(self, instance, validated_data):
        instance.user_data = validated_data.get('user_data', instance.user_data)
        instance.artist_count = validated_data.get('artist_count', instance.artist_count)
        instance.recommended_artists = validated_data.get('recommended_artists', instance.recommended_artists)
        instance.save()
        return instance


# Used to update or return an authenticated users details
class CurrentUserSerializer(geo_serializers.GeoFeatureModelSerializer):

    class Meta:
        model = get_user_model()
        geo_field = "last_location"
        fields = (
            "id", "username", "first_name", "last_name", "email")


# Overrides the rest-auth serializer to provide all-auth like registration functionality via api
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_settings.USERNAME_MIN_LENGTH,
        required=allauth_settings.USERNAME_REQUIRED
    )
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                _("The two password fields didn't match."))
        return data

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.save()
        return user
