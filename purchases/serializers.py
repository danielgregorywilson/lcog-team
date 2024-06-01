from rest_framework import serializers

from .models import Expense, ExpenseMonth
from people.serializers import SimpleEmployeeSerializer


class ExpenseSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Expense
        fields = [
            'url', 'pk', 'name', 'date', 'description', 'vendor', 'job', 'gls',
            'purchaser', 'receipt', 'approver', 'approved_at', 'status'
            
        ]

    purchaser = SimpleEmployeeSerializer(required=False)
    approver = SimpleEmployeeSerializer(required=False)


class ExpenseMonthSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ExpenseMonth
        fields = [
            'url', 'pk', 'employee', 'month', 'year', 'status', 'expenses'
        ]

    employee = SimpleEmployeeSerializer(required=False)
    expenses = ExpenseSerializer(many=True, read_only=True)