import traceback

from rest_framework import status, viewsets
from rest_framework.response import Response

from mainsite.helpers import record_error
from people.models import Employee
from purchases.models import Expense
from purchases.serializers import ExpenseSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    """
    API endpoint for credit card expenses.
    """
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated: 
            if user.is_superuser:
                return super().get_queryset()
            start = self.request.query_params.get('start', None)
            end = self.request.query_params.get('end', None)
            if start and end:
                return Expense.objects.filter(
                    purchaser=self.request.user.employee,
                    date__range=[start, end]
                )
            return Expense.objects.filter(purchaser=self.request.user.employee)
        else:
            return Expense.objects.none()

    def update(self, request, pk=None):
        """
        Update the expense with the given pk.
        """
        try:
            expense = Expense.objects.get(pk=pk)

            if expense.purchaser is None:
                expense.purchaser = request.user.employee

            expense.name = request.data.get('name', expense.name)
            expense.date = request.data.get('date', expense.date)
            expense.job = request.data.get('job', expense.job)
            expense.gls = request.data.get('gls', expense.gls)

            current_approver = expense.approver
            new_approver = request.data.get('approver')
            if current_approver is None and new_approver is None:
                pass
            else:
                current_pk = None
                if current_approver is not None:
                    current_pk = current_approver.pk
                new_pk = new_approver.get('pk', None)
                if current_pk != new_pk:
                    if new_pk == -1:
                        expense.approver = None
                    else:
                        expense.approver = Employee.objects.get(pk=new_pk)
            
            expense.approval_notes = request.data.get(
                'approval_notes', expense.approval_notes
            )

            expense.save()
            serialized_expense = ExpenseSerializer(
                expense, context={'request': request}
            )
            return Response(serialized_expense.data)

        except Exception as e:
            message = 'Error updating expense.'
            record_error(message, e, request, traceback.format_exc())
            return Response(
                data=message,
                status=status.HTTP_403_FORBIDDEN
            )
