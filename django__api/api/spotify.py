from social_django.utils import load_strategy
from rest_framework.response import Response
from rest_framework import status

from collections import Counter
import spotipy
import requests
import json

from . import serializers, views

# Spotify base URL
sp_base_url = 'https://api.spotify.com/'


def get_user_details(user):
    """
    Make a GET request to the spotify API for the users information
    :param user: currently validated user
    :return: Result in Json
    """
    serializer = serializers.SpotifySerializer
    social = user.social_auth.get(provider='spotify')
    social.refresh_token(load_strategy())
    auth_header = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(social.extra_data['access_token'])
    }
    try:
        res = requests.get(sp_base_url + 'v1/me', headers=auth_header)
        response = json.loads(res.content)
        serializer.update(serializer, user.spotify, {'user_data': response})
        return serializer

    except Exception as e:
        return Response({"detail": e}, status=status.HTTP_400_BAD_REQUEST)


def update_user_spotify_details(request, user):
    """
    Make a GET request to the spotify API for the users playlist information
    :param request: Incoming request
    :param user: currently validated user
    :return: Result in Json
    """
    serializer = serializers.SpotifySerializer
    social = user.social_auth.get(provider='spotify')
    social.refresh_token(load_strategy())
    token = social.extra_data['access_token']
    username = social.uid
    try:
        if token:
            sp = spotipy.Spotify(auth=token)
            playlists = sp.user_playlists(username)
            artist_list = build_artist_list(sp, playlists, username)

            # Create a unique dictionary of all artists and track counts
            artist_count = dict(Counter(artist_list))

            artist_count, favourite_artists = limit_artist_count_build_favourites(
                artist_count, user.spotify.recommended_artists)
            # Clean data retreive from spotify
            artist_count = remove_malformed_entries(artist_count)
            # Serializer used to update the Spotify table
            serializer.update(serializer, user.spotify,
                              {'artist_count': artist_count,
                               "recommended_artists": favourite_artists})
        else:
            print('No token found for user: {}'.format(user))
            views.get_users_spotify_details(request)

        return Response(artist_count, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": e}, status=status.HTTP_400_BAD_REQUEST)


def build_artist_list(sp, playlists, username):
    artist_list = []
    for playlist in playlists['items']:
        results = sp.user_playlist(username, playlist['id'], fields='tracks, next')
        tracks = results['tracks']
        tracks_items = tracks['items']

        if tracks['next'] is None:
            for track in tracks_items:
                artist_list.append(track['track']['artists'][0]['name'])

        else:
            while tracks['next']:
                tracks = sp.next(tracks)
                tracks_items.extend(tracks['items'])

            for track in tracks_items:
                artist_list.append(track['track']['artists'][0]['name'])
    return artist_list


def limit_artist_count_build_favourites(artist_count, favourite_artists):
    # Limit count to 10
    for k, v in artist_count.items():
        if v > 10:
            artist_count[k] = 10
        if v >= 4 and k not in favourite_artists:
            favourite_artists.append(k)
    return artist_count, favourite_artists


def remove_malformed_entries(artist_count):
    try:
        artist_count.pop('"')
    except KeyError:
        print('No quotation entries in this profile\n')
    try:
        artist_count.pop('')
    except KeyError:
        print('No blank entries in this profile\n')
    try:
        artist_count.pop(' ')
    except KeyError:
        print('No space entries, in this profile\n')
    return artist_count
