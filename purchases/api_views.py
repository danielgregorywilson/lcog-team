import datetime
import traceback

from django.db.models import Q
from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from mainsite.helpers import record_error
from people.models import Employee
from purchases.helpers import (
    send_submitter_denial_notification,
    send_submitter_monthly_expenses_reminders
)
from purchases.models import (
    Expense, ExpenseCard, ExpenseGL, ExpenseMonth, ExpenseStatement
)
from purchases.serializers import (
    ExpenseGLSerializer, ExpenseMonthSerializer, ExpenseSerializer,
    ExpenseStatementSerializer
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
            return ExpenseGL.objects.filter(
                expense__purchaser=self.request.user.employee
            )
        else:
            return ExpenseGL.objects.none()

    @action(detail=True, methods=['put'])
    def approver_approve(self, request, pk=None):
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
            gl.approved_at = timezone.now()
            if approve:
                gl.approved = True
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
                gl.approver_note = request.data.get('deny_note', '')
                gl.save()
                # Deny the expense
                expense.status = Expense.STATUS_APPROVER_DENIED
                expense.save()
                # Deny the month
                em.status = ExpenseMonth.STATUS_APPROVER_DENIED
                em.save()
                send_submitter_denial_notification(em.purchaser)
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
                expense.amount != request.data.get('amount') or
                expense.vendor != request.data.get('vendor') or
                expense.job != request.data.get('job')
            ):
                expense_fields_changed = True
            
            expense.name = request.data.get('name', expense.name)
            expense.date = request.data.get('date', expense.date)
            expense.amount = request.data.get('amount', expense.amount)
            expense.vendor = request.data.get('vendor', expense.vendor)
            expense.job = request.data.get('job', expense.job)
            expense.repeat = request.data.get('repeat', expense.repeat)
            
            gl_pks = []

            # Update all the GLs
            for gl in request.data.get('gls'):
                pk = gl.get('pk', None)
                code = gl.get('code', None)
                amount = gl.get('amount', None)
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
                        expense_gl.amount != amount or
                        expense_gl.approver != approver
                    ):
                        gl_changed = True
                    if gl_changed or expense_fields_changed:
                        expense_gl.approved = False
                        expense_gl.approved_at = None
                else:
                    expense_gl = ExpenseGL.objects.create(expense=expense)
                expense_gl.code = code
                expense_gl.amount = amount
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
            director = self.request.query_params.get('director', None)
            
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
            
            # Division Director getting all expense months
            if director:
                employeePK = self.request.query_params.get('employeePK', None)
                if year and month:
                    if employeePK:
                        return ExpenseMonth.objects.filter(
                            card__requires_director_approval=True,
                            card__director=user.employee,
                            purchaser__pk=employeePK, year=year, month=month
                        )
                    return ExpenseMonth.objects.filter(
                        card__requires_director_approval=True,
                        card__director=user.employee, year=year, month=month
                    )
                if employeePK:
                    return ExpenseMonth.objects.filter(
                        card__requires_director_approval=True,
                        card__director=user.employee, purchaser__pk=employeePK
                    )
                return ExpenseMonth.objects.filter(
                    card__requires_director_approval=True,
                    card__director=user.employee
                )

            # Employee getting own expense months
            if year and month:
                return ExpenseMonth.objects.filter(
                    purchaser=user.employee, year=year, month=month
                )
            return ExpenseMonth.objects.filter(purchaser=user.employee)
        else:
            return Expense.objects.none()

    def create(self, request, *args, **kwargs):
        month = request.data.get('month', None)
        year = request.data.get('year', None)
        if month is not None and year is not None:
            em = ExpenseMonth.objects.get_or_create(
                purchaser=request.user.employee,
                year=year,
                month=month
            )[0]

        # Create repeated expenses from last month
        last_month = month - 1
        last_year = year
        if last_month == 0:
            last_month = 12
            last_year -= 1
        last_em = ExpenseMonth.objects.filter(
            purchaser=request.user.employee,
            year=last_year,
            month=last_month
        ).first()
        if last_em:
            for expense in last_em.expenses.filter(repeat=True):
                new_expense = Expense.objects.create(
                    month=em,
                    name=expense.name,
                    date=expense.date.replace(year=year, month=month),
                    amount=expense.amount,
                    vendor=expense.vendor,
                    job=expense.job,
                    repeat=True
                )
                for gl in expense.gls.all():
                    ExpenseGL.objects.create(
                        expense=new_expense,
                        code=gl.code,
                        amount=gl.amount,
                        approver=gl.approver
                    )

        serialized_em = ExpenseMonthSerializer(
            em, context={'request': request})
        return Response(serialized_em.data)

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
                    if all([
                        em.director_approved,
                        em.director_approved_at is not None
                    ]):
                        # If expense month has been approved by director,
                        # mark as such.
                        em.status = ExpenseMonth.STATUS_DIRECTOR_APPROVED
                        em.fiscal_approved_at = None # Reset fiscal approval
                    else:
                        # If all expenses are approved by approver,
                        # mark as such.
                        em.status = ExpenseMonth.STATUS_APPROVER_APPROVED
                        # Reset director approval
                        em.director_approved_at = None
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
    def set_card(self, request, pk):
        """
        Set the expense card for an expense month.
        """
        try:
            em = ExpenseMonth.objects.get(pk=pk)
            card_pk = request.data.get('cardPk', None)
            if card_pk is not None:
                card = ExpenseCard.objects.get(pk=card_pk)
                em.card = card
                em.save()
                serialized_em = ExpenseMonthSerializer(
                    em, context={'request': request}
                )
                return Response(serialized_em.data)
            else:
                message = 'Didn\'t get a card PK. Cannot set card for EM'
                record_error(message, e, request, traceback.format_exc())
                return Response(
                    data=message,
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            message = 'Error setting card for expense month.'
            record_error(message, e, request, traceback.format_exc())
            return Response(
                data=message,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['put'])
    def director_approve(self, request, pk):
        """
        Director approves a month of expenses.
        """
        try:
            em = ExpenseMonth.objects.get(pk=pk)
            approve = request.data.get('approve', True)
            em.director_approved = approve
            em.director_approved_at = timezone.now()
            if approve:
                em.director_note = ''
                em.status = Expense.STATUS_DIRECTOR_APPROVED
            else:
                em.director_note = request.data.get('deny_note', '')
                em.status = Expense.STATUS_DIRECTOR_DENIED
                send_submitter_denial_notification(em.purchaser)
            em.save()
            serialized_em = ExpenseMonthSerializer(
                em, context={'request': request}
            )
            return Response(serialized_em.data)

        except Exception as e:
            message = 'Error director approving expense month.'
            record_error(message, e, request, traceback.format_exc())
            return Response(
                data=message,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['put'])
    def fiscal_approve(self, request, pk):
        """
        Fiscal approves a month of expenses.
        """
        try:
            em = ExpenseMonth.objects.get(pk=pk)
            approve = request.data.get('approve', True)
            em.fiscal_approver = request.user.employee
            em.fiscal_approved_at = timezone.now()
            if approve:
                em.fiscal_note = ''
                em.status = Expense.STATUS_FISCAL_APPROVED
            else:
                em.fiscal_note = request.data.get('deny_note', '')
                em.status = Expense.STATUS_FISCAL_DENIED
                # Reset director approval
                em.director_approved = False
                em.director_approved_at = None
                send_submitter_denial_notification(em.purchaser)
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


class ExpenseStatementViewSet(viewsets.ModelViewSet):
    """
    API endpoint for credit card expense statements.
    """
    queryset = ExpenseStatement.objects.all()
    serializer_class = ExpenseStatementSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated: 
            if user.is_superuser:
                return super().get_queryset()
            year = self.request.query_params.get('year', None)
            month = self.request.query_params.get('month', None)
            card = self.request.query_params.get('card', None)
            can_charge_to_card = Q(card__assignee=user.employee) | \
                Q(card__shared=True)
            if year and month:
                if card:
                    if user.employee.is_fiscal_employee:
                        return ExpenseStatement.objects.filter(
                            card__last4=card,
                            year=year,
                            month=month
                        )
                    else:
                        return ExpenseStatement.objects.filter(
                            can_charge_to_card,
                            card__last4=card,
                            year=year,
                            month=month
                        )
                else:
                    if user.employee.is_fiscal_employee:
                        return ExpenseStatement.objects.filter(
                            year=year, month=month
                        )
                    return ExpenseStatement.objects.filter(
                        can_charge_to_card, year=year, month=month
                    )
            else:
                if user.employee.is_fiscal_employee:
                    return ExpenseStatement.objects.all()
                else:
                    return ExpenseStatement.objects.filter(can_charge_to_card)
        else:
            return Expense.objects.none()

    @action(detail=False, methods=['get'])
    def send_notifications(self, request):
        """
        Send notifications to cardholders that statements have been uploaded.
        """
        try:
            num_recipients = send_submitter_monthly_expenses_reminders()
            return Response(
                f'Sent notifications to {num_recipients} cardholders.'
            )
        except Exception as e:
            message = 'Error sending notifications for expense statements.'
            record_error(message, e, request, traceback.format_exc())
            return Response(
                data=message,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )