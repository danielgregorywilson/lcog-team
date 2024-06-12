import datetime
import traceback

from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from mainsite.helpers import record_error
from people.models import Employee
from purchases.models import Expense, ExpenseGL, ExpenseMonth
from purchases.serializers import (
    ExpenseGLSerializer, ExpenseMonthSerializer, ExpenseSerializer
)

def all_expense_gls_approved(expense):
    """
    Check if all GLs for the given expense are approved.
    """
    return all(gl.approved for gl in expense.gls.all())

def all_month_expenses_approved(em):
    """
    Check if all expenses in the given expense month are approved.
    """
    return all(
        expense.status == Expense.STATUS_APPROVER_APPROVED
            for expense in em.expenses.all()
    )


class ExpenseGLViewSet(viewsets.ModelViewSet):
    """
    API endpoint for credit card expense general ledger entries.
    """
    queryset = ExpenseGL.objects.all()
    serializer_class = ExpenseGLSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated: 
            if user.is_superuser:
                return super().get_queryset()
            
            approve = self.request.query_params.get('approve', None)
            # Approver getting all Expense GLs to approve
            if approve:
                year = self.request.query_params.get('year', None)
                month = self.request.query_params.get('month', None)
                if year and month:
                    return ExpenseGL.objects.filter(
                        approver=user.employee,
                        expense__month__year=year,
                        expense__month__month=month,
                        expense__month__status__in=[
                            Expense.STATUS_SUBMITTED,
                            Expense.STATUS_APPROVER_APPROVED,
                            Expense.STATUS_APPROVER_DENIED
                        ]
                    )
                else:
                    return ExpenseGL.objects.filter(
                        approver=user.employee,
                        expense__month__status__in=[
                            Expense.STATUS_SUBMITTED,
                            Expense.STATUS_APPROVER_APPROVED,
                            Expense.STATUS_APPROVER_DENIED
                        ]
                    )
            
            # start = self.request.query_params.get('start', None)
            # end = self.request.query_params.get('end', None)
            # if start and end:
            #     return Expense.objects.filter(
            #         purchaser=self.request.user.employee,
            #         date__range=[start, end]
            #     )
            return ExpenseGL.objects.filter(
                expense__purchaser=self.request.user.employee
            )
        else:
            return ExpenseGL.objects.none()

    # def create(self, request, *args, **kwargs):
    #     code = request.data.get('code', None)
    #     percent = request.data.get('percent', None)
    #     approver = request.data.get('approver', None)
    #     if code is not None:
    #         expense_gl = ExpenseGL.objects.create(
    #             code=code, percent=percent, approver=approver
    #         )
    #         serialized_expense_gl = ExpenseGLSerializer(
    #             expense_gl, context={'request': request}
    #         )
    #         return Response(serialized_expense_gl.data)
    #     else:
    #         return Response(
    #             data='Error creating expense GL entry.',
    #             status=status.HTTP_500_INTERNAL_SERVER_ERROR
    #         )

    # def update(self, request, pk=None):
    #     """
    #     Update the expense GL entry with the given pk.
    #     """
    #     try:
    #         expense_gl = ExpenseGL.objects.get(pk=pk)
    #         code = request.data.get('code', expense_gl.code)
    #         percent = request.data.get('percent', expense_gl.percent)
    #         approver = request.data.get('approver', expense_gl.approver)
    #         expense_gl.code = code
    #         expense_gl.percent = percent
    #         expense_gl.approver = approver
    #         expense_gl.save()
    #         serialized_expense_gl = ExpenseGLSerializer(
    #             expense_gl, context={'request': request}
    #         )
    #         return Response(serialized_expense_gl.data)

    #     except Exception as e:
    #         message = 'Error updating expense GL entry.'
    #         record_error(message, e, request, traceback.format_exc())
    #         return Response(
    #             data=message,
    #             status=status.HTTP_500_INTERNAL_SERVER_ERROR
    #         )

    @action(detail=True, methods=['put'])
    def approve(self, request, pk=None):
        """
        Approver approves an Expense GL.
        """
        try:
            gl = ExpenseGL.objects.get(pk=pk)
            expense = gl.expense
            approve = request.data.get('approve', True)
            em = ExpenseMonth.objects.get_or_create(
                purchaser=expense.month.purchaser, year=expense.date.year,
                month=expense.date.month
            )[0]
            if approve:
                gl.approved = True
                gl.approved_at = timezone.now()
                gl.save()
                # If all GLs for the expense are approved, approve the expense
                if all(gl.approved for gl in expense.gls.all()):
                    expense.status = Expense.STATUS_APPROVER_APPROVED
                    expense.save()
                # If all expenses for the month are approved, approve the month
                if all_month_expenses_approved(em):
                    em.status = ExpenseMonth.STATUS_APPROVER_APPROVED
                    em.save()
            else:
                gl.approved = False
                gl.approved_at = timezone.now()
                gl.approver_note = request.data.get('deny_note', '')
                gl.save()
                # Deny the expense
                expense.status = Expense.STATUS_APPROVER_DENIED
                expense.save()
                # Deny the month
                em.status = ExpenseMonth.STATUS_APPROVER_DENIED
                em.save()
            # Return the updated expense
            serialized_gl = ExpenseGLSerializer(
                gl, context={'request': request}
            )
            return Response(serialized_gl.data)

        except Exception as e:
            message = 'Error approving expense.'
            record_error(message, e, request, traceback.format_exc())
            return Response(
                data=message,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ExpenseViewSet(viewsets.ModelViewSet):
    """
    API endpoint for credit card expenses.
    """
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def create(self, request, *args, **kwargs):
        date = request.data.get('date', None)
        if date is not None:
            date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        else: 
            date = datetime.date.today()
        em = ExpenseMonth.objects.get_or_create(
            purchaser=request.user.employee,
            year=date.year,
            month=date.month
        )[0]
        expense = Expense.objects.create(month=em, date=date)
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
                    month__purchaser=self.request.user.employee,
                    date__range=[start, end]
                )
            else:
                return Expense.objects.filter(
                    month__purchaser=self.request.user.employee
                )
        else:
            return Expense.objects.none()

    def update(self, request, pk):
        """
        Submitter updates an expense.
        """
        try:
            expense = Expense.objects.get(pk=pk)

            expense_fields_changed = False
            if (
                expense.name != request.data.get('name') or
                expense.date != request.data.get('date') or
                expense.description != request.data.get('description') or
                expense.vendor != request.data.get('vendor') or
                expense.job != request.data.get('job')
            ):
                expense_fields_changed = True
            
            expense.name = request.data.get('name', expense.name)
            request_date = request.data.get('date', None)
            if request_date is not None and request_date != '':
                expense.date = request.data.get('date')
                # If the month has changed, update the ExpenseMonth
                current_em = expense.month
                new_year, new_month, new_date = \
                    request.data.get('date', None).split('-')
                new_em = ExpenseMonth.objects.get_or_create(
                    purchaser=request.user.employee,
                    year=new_year,
                    month=new_month
                )[0]
                if current_em != new_em:
                    expense.month = new_em
            expense.description = request.data.get(
                'description', expense.description
            )
            expense.vendor = request.data.get('vendor', expense.vendor)
            expense.job = request.data.get('job', expense.job)
            
            gl_pks = []

            # Update all the GLs
            for gl in request.data.get('gls'):
                pk = gl.get('pk', None)
                code = gl.get('code', None)
                percent = gl.get('percent', None)
                approver_obj = gl.get('approver')
                if not approver_obj:
                    approver_obj = {
                        'pk': -1, 'name': '', 'legal_name': '', 'title': ''
                    }
                approver = None
                if approver_obj['pk'] != -1:
                    approver = Employee.objects.get(pk=approver_obj['pk'])
                
                if pk is not None:
                    expense_gl = ExpenseGL.objects.get(pk=pk)
                    # If any of the fields have changed, unapprove the GL
                    gl_changed = False
                    if (
                        expense_gl.code != code or
                        expense_gl.percent != percent or
                        expense_gl.approver != approver
                    ):
                        gl_changed = True
                    if gl_changed or expense_fields_changed:
                        expense_gl.approved = False
                        expense_gl.approved_at = None
                else:
                    expense_gl = ExpenseGL.objects.create(expense=expense)
                expense_gl.code = code
                expense_gl.percent = percent
                expense_gl.approver = approver
                
                expense_gl.save()
                gl_pks.append(expense_gl.pk)
            
            # Delete any GLs that were removed
            for gl in expense.gls.all():
                if gl.pk not in gl_pks:
                    gl.delete()

            # Set the expense to status draft for re-approval
            # in case it was previously approved.
            expense.status = Expense.STATUS_DRAFT

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
    def clear_approvals(self, request, pk):
        """
        Submitter clears approvals for an expense when uploading a new receipt.
        """
        try:
            # Clear Expense approval
            expense = Expense.objects.get(pk=pk)
            expense.status = Expense.STATUS_DRAFT
            expense.save()
            # Clear GL approvals
            for gl in expense.gls.all():
                gl.approved = False
                gl.approved_at = None
                gl.save()
            # Return the updated expense
            serialized_expense = ExpenseSerializer(
                expense, context={'request': request}
            )
            return Response(serialized_expense.data)
        except Exception as e:
            message = 'Error clearing approvals for expense.'
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
                            purchaser__pk=employeePK, year=year, month=month,
                        )
                    return ExpenseMonth.objects.filter(year=year, month=month)
                if employeePK:
                    return ExpenseMonth.objects.filter(
                        purchaser__pk=employeePK
                    )
                return ExpenseMonth.objects.all()
            # Employee getting own expense months
            if year and month:
                return ExpenseMonth.objects.filter(
                    purchaser=user.employee, year=year, month=month
                )
            return ExpenseMonth.objects.filter(purchaser=user.employee)
        else:
            return Expense.objects.none()

    @action(detail=False, methods=['post'])
    def submit(self, request):
        """
        Submitter submits a month of expenses.
        """
        year = request.data['yearInt']
        month = request.data['monthInt']
        note = request.data.get('note', '')
        unsubmit = request.data.get('unsubmit', False)
        try:
            em = ExpenseMonth.objects.get_or_create(
                purchaser=request.user.employee, year=year, month=month
            )[0]

            # MONTH
            if unsubmit:
                em.status = ExpenseMonth.STATUS_DRAFT
            else:
                if all_month_expenses_approved(em):
                    em.status = ExpenseMonth.STATUS_APPROVER_APPROVED
                else:
                    em.status = ExpenseMonth.STATUS_SUBMITTED
                em.submitter_note = note
            em.save()
            
            # EXPENSES
            # If we're submitting, submit all the expenses.
            # If we're unsubmitting, leave them as is.
            for expense in em.expenses.all():
                if not unsubmit:
                    if all_expense_gls_approved(expense):
                        expense.status = Expense.STATUS_APPROVER_APPROVED
                    else:
                        expense.status = Expense.STATUS_SUBMITTED
                expense.save()

                # GLS
                # If we're submitting, and any GL is rejected, mark as draft.
                for gl in expense.gls.all():
                    if all([
                        not unsubmit,
                        not gl.approved,
                        gl.approved_at is not None
                    ]):
                        gl.approved_at = None
                        gl.save()
            
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
    def approve(self, request, pk):
        """
        Fiscal approves a month of expenses.
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
