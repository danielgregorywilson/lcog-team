from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Route, Stop
from .serializers import MealStopSerializer
from mainsite.api_views import LargeResultsSetPagination
from mainsite.helpers import get_lat_long
from mainsite.models import City, ZipCode


class MealStopPermission(BasePermission):
    """
    Manager or employee may update the Performance Review.
    Others may read only.
    """

    def has_object_permission(self, request, view, obj):
        # Read and modify permissions are allowed with the relevant permission groups.
        if request.method in SAFE_METHODS:
            request.user.has_perm('meals.view_stop')
        else:
            request.user.groups.filter(name='Manage Meals on Wheels Stops').exists()


class MealStopViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Meals on Wheels Stops.
    """
    queryset = Stop.objects.all()
    serializer_class = MealStopSerializer
    permission_classes = [MealStopPermission]
    pagination_class = LargeResultsSetPagination

    def create(self, request):
        # TODO: Re-enable this permission check.
        # if not request.user.groups.filter(name='Manage Meals on Wheels Stops').exists():
        #     return Response({'created': False, 'error': 'You do not have permission to create a new stop.'})
        city = City.objects.get(name=request.data['city'])
        meal_type = Stop.TYPE_CHOICE_HOT if request.data['meal_type'] == 'Hot' else Stop.TYPE_CHOICE_COLD
        route_name = 'PU' if request.data['route_name'] in ['hotPU', 'coldPU'] else request.data['route_name']
        route = Route.objects.get(name=route_name)
        zip_code = ZipCode.objects.get(code=request.data['zip_code'])
        meal_stop = Stop.objects.create(
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
            address=request.data['address'],
            city=city,
            zip_code=zip_code,
            meal_type=meal_type,
            waitlist=request.data['waitlist'],
            phone=request.data['phone'],
            phone_notes=request.data['phone_notes'],
            notes=request.data['notes'],
            route=route
        )
        serialized_stop = MealStopSerializer(
            meal_stop, context={'request': request}
        )
        return Response({**serialized_stop.data, 'created': True})


class AddressLatLong(APIView):
    def get(self, request):
        latitude, longitude = get_lat_long(
            request.GET['address'], request.GET['city'], request.GET['state'],
            request.GET['zip']
        )
        return JsonResponse({'lat': latitude, 'long': longitude})