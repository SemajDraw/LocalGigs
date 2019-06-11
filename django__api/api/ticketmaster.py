from datetime import datetime, timedelta
from django.contrib.gis.geoip2 import GeoIP2
from iteration_utilities import Iterable
from background_task import background
from django.contrib.auth.models import User
import calendar
import ticketpy
from api import serializers
from django.conf import settings
import time
import json
import requests


# Token for Ticketmaster App and base url
tm_token = settings.TM_APP_KEY
tm_rec_token = settings.TM_REC_KEY
tm_base_url = 'https://app.ticketmaster.com/discovery/v2/'


def search_ticketmaster(request):

    try:
        classification_name = request.GET.get("search", "music")
    except:
        classification_name = "music"

    user_lat, user_long = request_latlong(request)

    return get_ticketmaster_events(user_lat, user_long, classification_name)


def get_ticketmaster_events(user_lat, user_long, classification_name):

    start_date_time, end_date_time = get_event_dates()
    try:
        if classification_name == "music":
            pages = load_events_classification(classification_name, start_date_time,
                                               end_date_time, user_lat, user_long)
        else:
            pages = search_events_keyword(classification_name, user_lat, user_long)

        single_page = []
        for index, page in zip(range(5), pages):
            for event in page:
                single_page.append(event)
            time.sleep(0.2)

        # for page in pages:
        #     # single_page.append(page)
        #     for event in page:
        #         single_page.append(event)
        #     time.sleep(1)

        event_list = event_list_builder(single_page)

        return event_list

    except Exception as e:
        print('Ticketmaster error: {}'.format(e))
        return {"error": "Couldnt connect to spotify api"}


def load_events_classification(classification_name, start_date_time, end_date_time, user_lat, user_long):

    tm_client = ticketpy.ApiClient(tm_rec_token)
    try:
        pages = tm_client.events.find(
            classification_name=classification_name,
            start_date_time=start_date_time,
            end_date_time=end_date_time,
            latlong=[user_lat, user_long],
            radius=50,
            unit='km'
        )
        return pages
    except Exception as e:
        print('Couldnt connect to tickermaster, error {}'.format(e))


def search_events_keyword(classification_name, user_lat, user_long):

    tm_client = ticketpy.ApiClient(tm_token)
    try:
        pages = tm_client.events.find(
            keyword=classification_name,
            latlong=[user_lat, user_long],
            radius=50,
            unit='km'
        )
        return pages
    except Exception as e:
        print('Couldnt connect to tickermaster, error {}'.format(e))


def event_list_builder(page):

    event_list = []
    for item in page:
        name = item.name
        spotify_url = build_spotify_url(name)

        # Checks if its the same event just with different tickets
        if 'ticket' in name.lower() or ' vip' in name.lower():
            continue

        date = format_date(item.local_start_date)

        # These values may not exist
        try:
            image = item.json['images'][0]['url']
        except KeyError:
            image = "empty"

        try:
            venue_url = item.json['_embedded']['venues'][0]['url']
        except KeyError:
            venue_url = "https://www.ticketmaster.ie/"

        try:
            yt_url = item.json['_embedded']['attractions'][0]['externalLinks']['youtube'][0]['url']
        except KeyError:
            yt_url = "https://www.youtube.com/"

        # Build event object
        event = {}
        try:
            event = {
                "name": name,
                "image": image,
                "date": date,
                "time": item.local_start_time,
                "venue": {
                    "name": item.json['_embedded']['venues'][0]['name'],
                    "city": item.json['_embedded']['venues'][0]['city']['name'],
                    "country": item.json['_embedded']['venues'][0]['country']['name'],
                    "address": item.json['_embedded']['venues'][0]['address'],
                    "longitude": item.json['_embedded']['venues'][0]['location']['longitude'],
                    "latitude": item.json['_embedded']['venues'][0]['location']['latitude'],
                    "venue_url": venue_url,
                },
                "youtube_url": yt_url,
                "ticketmaster_url": item.json['url'],
                "spotify_url": spotify_url
            }
        except Exception as e:
            print('Error: '.format(e))
            pass

        event_list.append(event)

    return event_list


def request_latlong(request):
    try:
        user_lat, user_long = get_user_latlong(request)
    except:
        user_lat, user_long = 53.350140, -6.266155

    return user_lat, user_long


def get_user_latlong(request):
    # Get the users location via IP in http request
    geo_ip = GeoIP2()
    ip = request.META.get('REMOTE_ADDR', None)

    try:
        if ip:
            geo_user = geo_ip.city(ip)
            user_lat = geo_user['latitude']
            user_long = geo_user['longitude']

        return user_lat, user_long
    except Exception as e:
        print('Ip could not be accessed, error: {}'.format(e))


def get_event_dates():
    # Get current time and date nd 1 year in the future
    date_time = datetime.now()
    start_date_time = datetime.strftime(date_time, "%Y-%m-%dT00:00:00Z")
    end_date_time = datetime.strftime(date_time + timedelta(days=100), "%Y-%m-%dT00:00:00Z")

    return start_date_time, end_date_time


def format_date(local_start_date):
    y, m, d = local_start_date.split('-')

    alphabetic_month = calendar.month_abbr[int(m)]

    return {'day': d, 'month': alphabetic_month}


def build_spotify_url(name):

    if name.split().__len__() > 1:
        url_name = Iterable(name.split(' ')).intersperse('%20').as_string('')
        spotify_url = "https://open.spotify.com/search/results/{}".format(url_name)
    else:
        spotify_url = "https://open.spotify.com/search/results/{}".format(name)

    return spotify_url


@background(schedule=1)
def update_recommended_events(user_id, user_ip):
    user = User.objects.get(pk=user_id)
    try:
        get_recommended_events(user, user_ip)
    except Exception as e:
        print(e)

    try:
        get_artist_recommendations(user)
        get_recommended_events(user, user_ip)
    except Exception as e:
        print(e)


def get_recommended_events(user, user_ip):
    try:
        serializer = serializers.ProfileSerializer
        recommended_events = user.profile.recommended_events
        recommended_artists = user.spotify.recommended_artists
        user_lat, user_long = request_latlong(user_ip)

        recommended_event_list = []
        for artist in recommended_artists:
            if len(artist) > 1:
                recommended_event_list.append(get_ticketmaster_events(user_lat, user_long, artist))
            time.sleep(0.2)

        flat_recommended_list = [event for event_list in recommended_event_list for event in event_list]

        updated_recommended_events = recommended_events
        [updated_recommended_events.append(event) for event in flat_recommended_list if
         event not in recommended_events]

        serializer.update(serializer, user.profile, {"recommended_events": updated_recommended_events})

    except Exception as e:
        print('Ticketmaster error: {}'.format(e))
        return {"error": "User has no saved artists"}


def get_artist_recommendations(user):

    try:
        serializer = serializers.SpotifySerializer
        user_artist_count = user.spotify.artist_count
        user_email = user.email
        recommended_artists = user.spotify.recommended_artists

        res = requests.post('http://34.244.186.50/api/get_recommendations/',
                            data={user_email: json.dumps(user_artist_count)})
        recommendations = json.loads(res.content)['recommended_artists']

        for artist in recommendations:
            if artist not in recommended_artists:
                recommended_artists.append(artist)

        serializer.update(serializer, user.spotify, {"recommended_artists": recommended_artists})
    except Exception as e:
        print(e)

