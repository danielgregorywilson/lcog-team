import datetime
import traceback

from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from mainsite.helpers import record_error
from people.models import Employee
from purchases.models import Expense, ExpenseMonth
from purchases.serializers import ExpenseMonthSerializer, ExpenseSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    """
    API endpoint for credit card expenses.
    """
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def create(self, request, *args, **kwargs):
        approver = None
        if request.user.employee.manager is not None:
            approver = request.user.employee.manager
        date = request.data.get('date', None)
        if date is not None:
            date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        else: 
            date = datetime.date.today()
        expense = Expense.objects.create(
            purchaser=request.user.employee,
            date=date,
            approver=approver
        )
        ExpenseMonth.objects.get_or_create(
            employee=request.user.employee,
            year=expense.date.year,
            month=expense.date.month
        )
        serialized_expense = ExpenseSerializer(
            expense, context={'request': request})
        return Response(serialized_expense.data)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated: 
            if user.is_superuser:
                return super().get_queryset()
            
            approve = self.request.query_params.get('approve', None)
            if approve:
                year = self.request.query_params.get('year', None)
                month = self.request.query_params.get('month', None)
                if year and month:
                    return Expense.objects.filter(
                        date__year=year,
                        date__month=month,
                        approver=user.employee,
                        status__in=[
                            Expense.STATUS_SUBMITTED,
                            Expense.STATUS_APPROVER_APPROVED,
                            Expense.STATUS_APPROVER_DENIED
                        ]
                    )
                else:
                    return Expense.objects.filter(
                        approver=user.employee,
                        status__in=[
                            Expense.STATUS_SUBMITTED,
                            Expense.STATUS_APPROVER_APPROVED,
                            Expense.STATUS_APPROVER_DENIED
                        ]
                    )
            
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
            expense.description = request.data.get(
                'description', expense.description
            )
            expense.vendor = request.data.get('vendor', expense.vendor)
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
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['put'])
    def approve(self, request, pk=None):
        """
        Approve the expense with the given pk.
        """
        try:
            expense = Expense.objects.get(pk=pk)
            approve = request.data.get('approve', True)
            if approve:
                expense.status = Expense.STATUS_APPROVER_APPROVED
                expense.approved_at = timezone.now()
                # If all expenses for the month are approved, approve the month
                em = ExpenseMonth.objects.get_or_create(
                    employee=expense.purchaser, year=expense.date.year,
                    month=expense.date.month
                )[0]
                em.status = ExpenseMonth.STATUS_APPROVER_APPROVED
                em.save()
            else:
                expense.status = Expense.STATUS_APPROVER_DENIED
            expense.save()
            serialized_expense = ExpenseSerializer(
                expense, context={'request': request}
            )
            return Response(serialized_expense.data)

        except Exception as e:
            message = 'Error approving expense.'
            record_error(message, e, request, traceback.format_exc())
            return Response(
                data=message,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ExpenseMonthViewSet(viewsets.ModelViewSet):
    queryset = ExpenseMonth.objects.all()
    serializer_class = ExpenseMonthSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated: 
            if user.is_superuser:
                return super().get_queryset()
            
            year = self.request.query_params.get('year', None)
            month = self.request.query_params.get('month', None)

            fiscal = self.request.query_params.get('fiscal', None)
            # Fiscal getting all expense months
            if fiscal:
                employeePK = self.request.query_params.get('employeePK', None)
                if year and month:
                    if employeePK:
                        return ExpenseMonth.objects.filter(
                            employee__pk=employeePK, year=year, month=month,
                            status__in=[
                                ExpenseMonth.STATUS_APPROVER_APPROVED,
                                ExpenseMonth.STATUS_FISCAL_APPROVED,
                                ExpenseMonth.STATUS_FISCAL_DENIED
                            ]
                        )
                    return ExpenseMonth.objects.filter(
                        year=year, month=month, status__in=[
                            ExpenseMonth.STATUS_APPROVER_APPROVED,
                            ExpenseMonth.STATUS_FISCAL_APPROVED,
                            ExpenseMonth.STATUS_FISCAL_DENIED
                        ]
                    )
                if employeePK:
                    return ExpenseMonth.objects.filter(
                        employee__pk=employeePK, status__in=[
                            ExpenseMonth.STATUS_APPROVER_APPROVED,
                            ExpenseMonth.STATUS_FISCAL_APPROVED,
                            ExpenseMonth.STATUS_FISCAL_DENIED
                        ]
                    )
                return ExpenseMonth.objects.filter(
                    status__in=[
                        ExpenseMonth.STATUS_APPROVER_APPROVED,
                        ExpenseMonth.STATUS_FISCAL_APPROVED,
                        ExpenseMonth.STATUS_FISCAL_DENIED
                    ]
                )
            # Employee getting own expense months
            if year and month:
                return ExpenseMonth.objects.filter(
                    employee=user.employee, year=year, month=month
                )
            return ExpenseMonth.objects.filter(employee=user.employee)
        else:
            return Expense.objects.none()

    @action(detail=False, methods=['post'])
    def submit(self, request):
        """
        Submit a month of expenses.
        """
        year = request.data['yearInt']
        month = request.data['monthInt']
        unsubmit = request.data.get('unsubmit', False)
        try:
            em = ExpenseMonth.objects.get_or_create(
                employee=request.user.employee, year=year, month=month
            )[0]
            if unsubmit:
                em.status = ExpenseMonth.STATUS_DRAFT
            else:
                em.status = ExpenseMonth.STATUS_SUBMITTED
            em.save()
            for expense in em.expenses:
                if unsubmit:
                    expense.status = Expense.STATUS_DRAFT
                else:
                    expense.status = Expense.STATUS_SUBMITTED
                expense.save()
            serialized_expense_month = ExpenseMonthSerializer(
                em, context={'request': request}
            )
            return Response(serialized_expense_month.data)
        except Exception as e:
            message = 'Error submitting expense month'
            record_error(message, e, request, traceback.format_exc())
            return Response(
                data=message,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(detail=True, methods=['put'])
    def approve(self, request, pk=None):
        """
        Approve the expense month with the given pk.
        """
        try:
            em = ExpenseMonth.objects.get(pk=pk)
            approve = request.data.get('approve', True)
            if approve:
                em.status = Expense.STATUS_FISCAL_APPROVED
                em.approver = request.user.employee
                em.approved_at = timezone.now()
            else:
                em.status = Expense.STATUS_FISCAL_DENIED
            em.save()
            serialized_em = ExpenseMonthSerializer(
                em, context={'request': request}
            )
            return Response(serialized_em.data)

        except Exception as e:
            message = 'Error approving expense month.'
            record_error(message, e, request, traceback.format_exc())
            return Response(
                data=message,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
