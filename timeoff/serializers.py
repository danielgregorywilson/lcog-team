from rest_framework import serializers

from timeoff.models import TimeOffRequest


class TimeOffRequestSerializer(serializers.HyperlinkedModelSerializer):
    employee_pk = serializers.IntegerField(source='employee.pk') #TODO: Make IntegerField
    employee_name = serializers.CharField(source='employee.user.get_full_name')
    manager_pk = serializers.IntegerField(source='employee.manager.pk')
 
    class Meta:
        model = TimeOffRequest
        fields = [
            'url', 'pk', 'employee_pk', 'employee_name', 'manager_pk',
            'start_date', 'end_date', 'note', 'acknowledged', 'created_at',
            'acknowledged_at'
        ]