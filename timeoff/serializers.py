import pdb
from rest_framework import serializers

from timeoff.models import TimeOffRequest


class TimeOffRequestSerializer(serializers.HyperlinkedModelSerializer):
    employee_pk = serializers.IntegerField(source='employee.pk') #TODO: Make IntegerField
    employee_name = serializers.CharField(source='employee.user.get_full_name')
    manager_pk = serializers.IntegerField(source='employee.manager.pk')
    dates = serializers.SerializerMethodField()
 
    class Meta:
        model = TimeOffRequest
        fields = [
            'url', 'pk', 'employee_pk', 'employee_name', 'manager_pk', 'dates',
            'note', 'acknowledged', 'created_at', 'acknowledged_at'
        ]

    @staticmethod
    def get_dates(timeoffrequest):
        for idx, date_obj in enumerate(timeoffrequest.dates):
            if type(date_obj) is str:
                timeoffrequest.dates[idx] = {'from': date_obj, 'to': date_obj}
        return timeoffrequest.dates
