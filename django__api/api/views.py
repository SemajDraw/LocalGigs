from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user_model
from rest_framework import permissions, authentication, status, generics
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from django.contrib.gis.geos import Point
from . import serializers
import requests
import json

# Token for Ticketmaster App and base url
tm_token = 'BabzejjEdlmaAhyC7DoWWAYyb8u66r5u'
tm_base_url = 'https://app.ticketmaster.com/discovery/v2/'


# Django-rest-auth classes
class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


# API login for mobile application that returns the users profile information
# and an authentication token
@api_view(["GET", ])
@permission_classes((permissions.AllowAny,))
# @csrf_exempt
def token_login(request):
    if (not request.GET["email"]) or (not request.GET["password"]):
        return Response({"detail": "Missing email and/or password"}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(email=request.GET["email"], password=request.GET["password"])
    if user:
        if user.is_active:
            login(request, user)
            try:
                my_token = Token.objects.get(user=user)
                username = user.first_name
                email = user.email
                firstName = user.first_name
                lastName = user.last_name
                age = user.profile.age
                gender = user.profile.gender
                bio = user.profile.bio
                return Response({"token": "{}".format(my_token.key),
                                 "first_name": "{}".format(firstName),
                                 "last_name": "{}".format(lastName),
                                 "username": "{}".format(username),
                                 "email": "{}".format(email),
                                 "age": "{}".format(age),
                                 "gender": "{}".format(gender),
                                 "bio": "{}".format(bio),
                                 },
                                status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"detail": "Could not get token"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Inactive account"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"detail": "Invalid User Id of Password"}, status=status.HTTP_400_BAD_REQUEST)


# Gets an authenticated users details from the BD and returns it
class UserDetails(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.CurrentUserSerializer

    def get_object(self):
        return get_user_model().objects.get(email=self.request.user.email)


# Allows an authenticated user to make a call to the Ticketmaster API with search and city parameters
# which return a response from which name, url, image, date, time, venue_id and youtube_url are extracted
# and returned as an array of objects.
@api_view(["GET", ])
@login_required
@permission_classes((permissions.IsAuthenticated,))
@authentication_classes((authentication.TokenAuthentication, authentication.SessionAuthentication))
def tm_get_events(request):
    """
    Make a GET request to the ticketmaster API with the strings entered by the user
    :param request: Incoming request search and city string
    :return: Result in Json
    """

    search = request.query_params.get("search", "")
    if search:
        search = search.lower()

    city = request.query_params.get("city", "")
    if city:
        city = city.lower()

    date_time = datetime.now()

    start_date_time = datetime.strftime(date_time, "%Y-%m-%dT00:00:00Z")
    end_date_time = datetime.strftime(date_time + timedelta(days=7), "%Y-%m-%dT00:00:00Z")

    try:
        response = requests.get(tm_base_url + 'events.json?classificationName=' + search +
                                '&city=' + city + '&startDateTime=' + start_date_time +
                                '&endDateTime=' + end_date_time + '&apikey=' + tm_token)
        response_content = json.loads(response.content)
        response_list = response_content['_embedded']['events']

        event_list = []
        for item in response_list:
            try:
                event = {
                    "name": item['name'],
                    "url": item['url'],
                    "image": item['images'][0]['url'],
                    "date": item['dates']['start']['localDate'],
                    "time": item['dates']['start']['localTime'],
                    "venue_id": item['_embedded']['venues'][0]['id'],
                    "youtube_url": item['_embedded']['attractions'][0]['externalLinks']['youtube'][0]['url']
                }
            except KeyError:
                event = {
                    "name": item['name'],
                    "url": item['url'],
                    "image": item['images'][0]['url'],
                    "date": item['dates']['start']['localDate'],
                    "time": item['dates']['start']['localTime'],
                    "venue_id": item['_embedded']['venues'][0]['id']
                }

            event_list.append(event)

        return Response(event_list, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"detail": e}, status=status.HTTP_400_BAD_REQUEST)


# Allows an authenticated user to make a call to the Ticketmaster API with venue_id as a parameter
# which return a response from which name, address, longlat, url, images are extracted
# and returned as an array of objects.
@api_view(["GET", ])
@login_required
@permission_classes((permissions.IsAuthenticated,))
@authentication_classes((authentication.TokenAuthentication, authentication.SessionAuthentication))
def tm_get_venue(request):
    """
    Make a GET request to the ticketmaster API with the strings entered by the user
    :param request: Incoming request venue_id string
    :return: Result in Json
    """

    venue_id = request.query_params.get("venue_id", "")

    try:
        response = requests.get(tm_base_url + 'venues/' + venue_id + '.json?apikey=' + tm_token)
        venue_object = json.loads(response.content)
        try:
            venue = {
                "name": venue_object['name'],
                "address": venue_object['address']['line1'],
                "longlat": venue_object['location'],
                "url": venue_object['url'],
                "images": venue_object['images']
            }
        except KeyError:
            venue = {
                "name": venue_object['name'],
                "address": venue_object['address']['line1'],
                "longlat": venue_object['location'],
                "url": venue_object['url']
            }

        return Response(venue, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"detail": e}, status=status.HTTP_400_BAD_REQUEST)


# Accepts PUT or PATCH request from and authenticated user that updates the last_location entry in the
# Profile table of the DB associated with them, type is a GEO point.
class UpdatePosition(generics.UpdateAPIView):
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.LastLocationSerializer

    def get_object(self):
        return get_user_model().objects.get(email=self.request.user.email)

    def perform_update(self, serializer, **kwargs):
        try:
            lat1 = float(self.request.data.get("lat", False))
            lon1 = float(self.request.data.get("long", False))
            lat2 = float(self.request.query_params.get("lat", False))
            lon2 = float(self.request.query_params.get("long", False))
            if lat1 and lon1:
                point = Point(lon1, lat1)
            elif lat2 and lon2:
                point = Point(lon2, lat2)
            else:
                point = None

            if point:
                serializer.instance.profile.last_location = point
                serializer.save()
            return serializer
        except:
            pass


# Accepts PUT or PATCH request from and authenticated user that updates the interested_html entry in the
# Profile table of the DB associated with the user, type is text.
class UpdateInterestedHTML(generics.UpdateAPIView):
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.InterestedHtmlSerializer

    def get_object(self):
        return get_user_model().objects.get(email=self.request.user.email)

    def perform_update(self, serializer, **kwargs):
        try:
            html = self.request.data.get("interested_html", False)
            serializer.instance.profile.interested_html = html
            serializer.save()
            return serializer
        except:
            pass

