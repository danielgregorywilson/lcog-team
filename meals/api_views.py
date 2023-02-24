from rest_framework import viewsets

from .models import Stop
from .serializers import MealStopSerializer


class MealStopViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Meals on Wheels Stops.
    """
    queryset = Stop.objects.all()
    serializer_class = MealStopSerializer
