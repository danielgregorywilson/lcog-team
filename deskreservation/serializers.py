from datetime import datetime

from django.utils.timezone import get_current_timezone

from rest_framework import serializers

from .models import Desk, DeskHold, DeskReservation


class DeskSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Desk
        fields = [
            'url', 'pk', 'building', 'floor', 'number', 'active', 'lead',
            'ergonomic', 'held_today'
        ]


class DeskReservationSerializer(serializers.HyperlinkedModelSerializer):
    employee_pk = serializers.SerializerMethodField()
    employee_name = serializers.SerializerMethodField()
    desk_building = serializers.CharField(source='desk.building')
    desk_floor = serializers.CharField(source='desk.floor')
    desk_number = serializers.CharField(source='desk.number')
    
    class Meta:
        model = DeskReservation
        fields = [
            'url', 'pk', 'employee_pk', 'employee_name', 'desk_building',
            'desk_floor', 'desk_number', 'check_in', 'check_out'
        ]

    @staticmethod
    def get_employee_pk(reservation):
        if reservation.employee:
            return reservation.employee.pk
        else:
            return ''

    @staticmethod
    def get_employee_name(reservation):
        if reservation.employee:
            return reservation.employee.name
        else:
            return ''