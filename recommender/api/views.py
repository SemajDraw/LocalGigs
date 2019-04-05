from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from . import recommendation


@api_view(['POST', ])
def get_recommendations(request):

    if request.method == 'POST':
        if not request.data:
            return Response({"detail": "Missing user info"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            recommended_artists = recommendation.generate_recommendations(request.data)
            return Response({'recommended_artists': recommended_artists}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
