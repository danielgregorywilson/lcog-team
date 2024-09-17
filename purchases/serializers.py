from rest_framework import serializers

from .models import (
    Expense, ExpenseCard, ExpenseGL, ExpenseMonth, ExpenseMonthLock,
    ExpenseStatement, ExpenseStatementItem
)
from people.serializers import SimpleEmployeeSerializer


class ExpenseGLSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ExpenseGL
        fields = [
            'url', 'pk', 'code', 'amount', 'approver', 'approved',
            'approved_at', 'approver_note', 'expense_name', 'expense_date',
            'expense_amount', 'expense_description', 'expense_vendor',
            'expense_job', 'expense_receipt', 'expense_purchaser',
            'expense_status', 'em_month', 'em_year', 'em_note'
        ]

    approver = SimpleEmployeeSerializer(required=False)
    expense_name = serializers.CharField(
        source='expense.name', read_only=True
    )
    expense_date = serializers.DateField(
        source='expense.date', read_only=True
    )
    expense_amount = serializers.DecimalField(
        source='expense.amount', read_only=True, max_digits=10,
        decimal_places=2
    )
    expense_description = serializers.DateField(
        source='expense.description', read_only=True
    )
    expense_vendor = serializers.CharField(
        source='expense.vendor', read_only=True
    )
    expense_job = serializers.CharField(
        source='expense.job', read_only=True
    )
    expense_receipt = serializers.SerializerMethodField()
    expense_purchaser = serializers.CharField(
        source='expense.month.purchaser.name', read_only=True
    )
    expense_status = serializers.CharField(
        source='expense.status', read_only=True
    )
    em_month = serializers.IntegerField(
        source='expense.month.month', read_only=True
    )
    em_year = serializers.IntegerField(
        source='expense.month.year', read_only=True
    )
    em_note = serializers.CharField(
        source='expense.month.submitter_note', read_only=True
    )

    def get_expense_receipt(self, obj):
        request = self.context.get('request')
        if obj.expense.receipt:
            return str(request.build_absolute_uri(obj.expense.receipt.url))
        return None


class ExpenseSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Expense
        fields = [
            'url', 'pk', 'name', 'date', 'amount', 'vendor', 'job', 'gls',
            'receipt', 'receipt_type', 'status', 'purchaser', 'repeat'
        ]

    gls = ExpenseGLSerializer(many=True, read_only=True)
    receipt_type = serializers.SerializerMethodField()
    purchaser = serializers.CharField(
        source='month.purchaser.name', read_only=True
    )

    @staticmethod
    def get_receipt_type(obj):
        # Returns 'image' or 'pdf' based on the file extension
        if obj.receipt:
            extension = obj.receipt.name.split('.')[-1]
            if extension in ['jpg', 'jpeg', 'png']:
                return 'image'
            elif extension == 'pdf':
                return 'pdf'
        return None


class ExpenseCardSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ExpenseCard
        fields = [
            'pk', 'last4', 'assignee', 'shared', 'display',
            'requires_director_approval', 'director_name'
        ]

    display = serializers.SerializerMethodField()
    director_name = serializers.CharField(
        source='director.name', read_only=True
    )

    @staticmethod
    def get_display(card):
        display = f'*{ card.last4 }'
        if card.shared:
            display += ' (Shared)'
        elif card.assignee:
            display += f' ({ card.assignee.name })'
        return display


class ExpenseStatementItemSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ExpenseStatementItem
        fields = ['pk', 'date', 'description', 'amount']


class ExpenseStatementSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ExpenseStatement
        fields = [
            'pk', 'card', 'month', 'year', 'items'
        ]

    card = ExpenseCardSerializer(required=False)
    items = ExpenseStatementItemSerializer(many=True, read_only=True)


class ExpenseMonthSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ExpenseMonth
        fields = [
            'url', 'pk', 'purchaser', 'month', 'year', 'card', 'statement',
            'expenses', 'submitter_note', 'director_approved',
            'director_approved_at', 'director_note', 'fiscal_approver',
            'fiscal_approved_at', 'fiscal_note', 'status'
        ]

    purchaser = SimpleEmployeeSerializer(required=False)
    card = ExpenseCardSerializer(required=False)
    statement = serializers.SerializerMethodField()
    expenses = ExpenseSerializer(many=True, read_only=True)
    fiscal_approver = SimpleEmployeeSerializer(required=False)
    
    def get_statement(self, obj):
        if obj.card:
            return ExpenseStatementSerializer(
                obj.card.statements.filter(
                    month=obj.month, year=obj.year
                ).first(),
                context=self.context
            ).data


class ExpenseMonthLockSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ExpenseMonthLock
        fields = ['pk', 'year', 'month', 'locked_at', 'locked_by']