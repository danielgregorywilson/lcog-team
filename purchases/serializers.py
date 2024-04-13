from rest_framework import serializers

from .models import Expense


class ExpenseSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Expense
        fields = [
            'url', 'pk', 'name', 'date', 'job', 'gls', 'purchaser', 'approver',
            'approval_notes', 'receipt'
        ]
