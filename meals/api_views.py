from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from .models import Stop
from .serializers import MealStopSerializer
from mainsite.api_views import LargeResultsSetPagination
from mainsite.helpers import get_lat_long


class MealStopViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Meals on Wheels Stops.
    """
    queryset = Stop.objects.all()
    serializer_class = MealStopSerializer
    pagination_class = LargeResultsSetPagination


class AddressLatLong(APIView):
    def get(self, request):
        latitude, longitude = get_lat_long(
            request.GET['address'], request.GET['city'], request.GET['state'],
            request.GET['zip']
        )
        return JsonResponse({'lat': latitude, 'long': longitude})