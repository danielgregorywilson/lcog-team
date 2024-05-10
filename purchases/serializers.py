from rest_framework import serializers

from .models import Expense
from people.serializers import SimpleEmployeeSerializer


class ExpenseSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Expense
        fields = [
            'url', 'pk', 'name', 'date', 'job', 'gls', 'purchaser', 'receipt',
            'approver', 'approved_at'
            
        ]

    purchaser = SimpleEmployeeSerializer(required=False)
    approver = SimpleEmployeeSerializer(required=False)
