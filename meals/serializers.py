from rest_framework import serializers

from .models import Stop


class MealStopSerializer(serializers.HyperlinkedModelSerializer):
    city = serializers.CharField(source='city.name')
    zip_code = serializers.CharField(source='zip_code.code')
    route = serializers.CharField(source='route.name')

    class Meta:
        model = Stop
        fields = (
            'first_name', 'last_name', 'address', 'city', 'zip_code',
            'latitude', 'longitude', 'meal_type', 'waitlist', 'phone',
            'phone_notes', 'notes', 'route', 'created_at', 'updated_at'
        )