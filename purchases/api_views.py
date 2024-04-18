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

    def update(self, request, pk=None):
        """
        Update the expense with the given pk.
        """
        try:
            e = Expense.objects.get(pk=pk)

            if e.purchaser is None:
                e.purchaser = request.user.employee

            e.name = request.data.get('name', e.name)
            e.date = request.data.get('date', e.date)
            e.job = request.data.get('job', e.job)
            e.gls = request.data.get('gls', e.gls)

            current_approver = e.approver
            new_approver = request.data.get('approver')
            if current_approver is None and new_approver is None:
                pass
            else:
                current_pk = current_approver.pk if current_approver is not None else None
                new_pk = new_approver.get('pk', None)
                if current_pk != new_pk:
                    if new_pk == -1:
                        e.approver = None
                    else:
                        e.approver = Employee.objects.get(pk=new_pk)
            
            e.approval_notes = request.data.get(
                'approval_notes', e.approval_notes
            )
            # e.receipt = request.data.get('receipt', e.receipt)

            e.save()
            serialized_expense = ExpenseSerializer(
                e, context={'request': request}
            )
            return Response(serialized_expense.data)

        except Exception as e:
            message = 'Error updating expense.'
            record_error(message, e, request, traceback.format_exc())
            return Response(
                data=message,
                status=status.HTTP_403_FORBIDDEN
            )

    # def get_queryset(self):
    #     """
    #     Return a list of all responsibilities to any authenticated user.
    #     Optionally filter by orphaned responsibilities.
    #     Optionally filter by employee pk to get primary responsibilities with
    #     secondaries, or just a list of secondaries.
    #     """
    #     import pdb; pdb.set_trace();
    #     user = self.request.user
    #     if user.is_authenticated:
    #         orphaned = self.request.query_params.get('orphaned', None)
    #         if orphaned is not None and orphaned == "true":
    #             queryset = Responsibility.objects.filter(
    #                 Q(primary_employee__isnull=True) | Q(secondary_employee__isnull=True)
    #             )
    #         employee = self.request.query_params.get('employee', None)
    #         if employee is not None and employee.isdigit():
    #             secondary = self.request.query_params.get('secondary', None)
    #             if secondary is not None and secondary == 'true':
    #                 queryset = Responsibility.objects.filter(secondary_employee=employee)
    #             else:
    #                 queryset = Responsibility.objects.filter(primary_employee=employee)
    #     else:
    #         queryset = Responsibility.objects.none()
    #     return queryset if 'queryset' in locals() else Responsibility.objects.all()
