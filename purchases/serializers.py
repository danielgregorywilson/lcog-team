from rest_framework import serializers

from .models import Expense, ExpenseGL, ExpenseMonth
from people.serializers import SimpleEmployeeSerializer


class ExpenseGLSerializer(serializers.HyperlinkedModelSerializer):

        class Meta:
            model = ExpenseGL
            fields = [
                'url', 'pk', 'code', 'percent', 'approver', 'approved',
                'approved_at', 'expense_name', 'expense_date',
                'expense_purchaser', 'expense_status'
            ]
    
        approver = SimpleEmployeeSerializer(required=False)
        expense_name = serializers.CharField(
            source='expense.name', read_only=True
        )
        expense_date = serializers.DateField(
            source='expense.date', read_only=True
        )
        expense_purchaser = serializers.CharField(
            source='expense.purchaser.name', read_only=True
        )
        expense_status = serializers.CharField(
            source='expense.status', read_only=True
        )


class ExpenseSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Expense
        fields = [
            'url', 'pk', 'name', 'date', 'description', 'vendor', 'job', 'gls',
            'purchaser', 'receipt', 'approver', 'approved_at', 'status'
            
        ]

    purchaser = SimpleEmployeeSerializer(required=False)
    approver = SimpleEmployeeSerializer(required=False)
    gls = ExpenseGLSerializer(many=True, read_only=True)


class ExpenseMonthSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ExpenseMonth
        fields = [
            'url', 'pk', 'employee', 'month', 'year', 'status', 'expenses'
        ]

    employee = SimpleEmployeeSerializer(required=False)
    expenses = ExpenseSerializer(many=True, read_only=True)