from rest_framework import serializers

from timeoff.models import TimeOffRequest
from people.models import Employee
from people.serializers import EmployeeSerializer


class TimeOffRequestSerializer(serializers.HyperlinkedModelSerializer):
    employee_pk = serializers.IntegerField(source='employee.pk')
    employee_name = serializers.CharField(source='employee.user.get_full_name')
    manager_pk = serializers.IntegerField(source='employee.manager.pk')
    conflicts = serializers.ListField(required=False)
 
    class Meta:
        model = TimeOffRequest
        fields = [
            'url', 'pk', 'employee_pk', 'employee_name', 'manager_pk',
            'start_date', 'end_date', 'note', 'acknowledged', 'created_at',
            'acknowledged_at', 'conflicts'
        ]


class ConflictingResponsibilitiesSerializer(EmployeeSerializer):
    responsibility_names = serializers.ListField()

    class Meta:
        model = Employee
        fields = [
            'pk', 'name', 'responsibility_names'
        ]