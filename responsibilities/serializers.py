
from rest_framework import serializers

from .models import Responsibility, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class ResponsibilitySerializer(serializers.HyperlinkedModelSerializer):
    tags = TagSerializer(many=True)
    primary_employee_pk = serializers.SerializerMethodField()
    primary_employee_name = serializers.SerializerMethodField()
    secondary_employee_pk = serializers.SerializerMethodField()
    secondary_employee_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Responsibility
        fields = [
            'url', 'pk', 'name', 'description', 'link', 'tags', 'primary_employee_pk',
            'primary_employee_name', 'secondary_employee_pk',
            'secondary_employee_name'
        ]

    @staticmethod
    def get_primary_employee_pk(responsibility):
        if responsibility.primary_employee:
            return responsibility.primary_employee.pk
        else:
            return ''

    @staticmethod
    def get_secondary_employee_pk(responsibility):
        if responsibility.secondary_employee:
            return responsibility.secondary_employee.pk
        else:
            return ''

    @staticmethod
    def get_primary_employee_name(responsibility):
        if responsibility.primary_employee:
            return responsibility.primary_employee.user.get_full_name()
        else:
            return ''
    
    @staticmethod
    def get_secondary_employee_name(responsibility):
        if responsibility.secondary_employee:
            return responsibility.secondary_employee.user.get_full_name()
        else:
            return ''
