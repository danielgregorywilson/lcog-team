from rest_framework import viewsets

from .models import Stop
from .serializers import MealStopSerializer
from mainsite.api_views import LargeResultsSetPagination


class MealStopViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Meals on Wheels Stops.
    """
    queryset = Stop.objects.all()
    serializer_class = MealStopSerializer
    pagination_class = LargeResultsSetPagination