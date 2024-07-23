from datetime import date, datetime, timedelta
import os

from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from mainsite.helpers import send_email
from people.models import Employee
from purchases.models import ExpenseMonth


def send_submitter_monthly_expenses_reminders():
    # After end of month on the 1st of the next month at 3PM
    # Submitter submitted last month and there's no draft for this month.
    # Submitter has an unsubmitted draft for this month.
    current_site = Site.objects.get_current()
    expenses_url = current_site.domain + '/expenses/submit'
    profile_url = current_site.domain + '/profile'
    
    html_template = \
        '../templates/email/expenses/submitter-monthly-reminder.html'

    today = datetime.now().date()
    # Current month is the month that just ended.
    # Previous month is the month before that.
    curr_month_date = today.replace(day=1) - timedelta(days=1)
    prev_month_date = curr_month_date.replace(day=1) - timedelta(days=1)
    month_before_that_date = prev_month_date.replace(day=1) - timedelta(days=1)
    curr_month_name = curr_month_date.strftime('%B')

    recipients = []
    subs = Employee.objects.filter(user__groups__name='Expense Submitter')
    for sub in subs:
        if sub.should_receive_email_of_type('expenses', ''):
            # Do they have an unsubmitted draft for this month?
            em = ExpenseMonth.objects.filter(
                purchaser=sub,
                year=curr_month_date.year,
                month=curr_month_date.month,
                status=ExpenseMonth.STATUS_DRAFT
            ).exists()
            if em:
                recipients.append([sub.user.email, 'draft'])
            else:
                # Did they submit last month or the month before,
                # but not this month?
                em_last_month = ExpenseMonth.objects.filter(
                    purchaser=sub, year=prev_month_date.year,
                    month=prev_month_date.month
                ).exists()
                em_month_before_that = ExpenseMonth.objects.filter(
                    purchaser=sub, year=month_before_that_date.year,
                    month=month_before_that_date.month
                ).exists()
                em_this_month = ExpenseMonth.objects.filter(
                    purchaser=sub, year=curr_month_date.year,
                    month=curr_month_date.month
                ).exists()
                if (
                    em_last_month or em_month_before_that
                ) and not em_this_month:
                    recipients.append([sub.user.email, 'last_month'])
    for recipient in recipients:
        html_message = render_to_string(html_template, { 'context': {
            'curr_month_name': curr_month_name,
            'message_type': recipient[1],
            'expenses_url': expenses_url,
            'profile_url': profile_url,
            'from_email': os.environ.get('FROM_EMAIL')
        }, })
        plaintext_message = strip_tags(html_message)
        send_email(
            recipient[0],
            f'Time to enter { curr_month_name } expenses',
            plaintext_message,
            html_message
        )
    
    return len(recipients)


def send_submitter_weekly_revise_reminders():
    # Every week on Friday at 3PM
    # Submitter needs to revise and resubmit
    current_site = Site.objects.get_current()
    expenses_url = current_site.domain + '/expenses/submit'
    profile_url = current_site.domain + '/profile'
    
    html_template = \
        '../templates/email/expenses/submitter-weekly-revise-reminder.html'

    recipients = []
    subs = Employee.objects.filter(user__groups__name='Expense Submitter')
    for sub in subs:
        if sub.should_receive_email_of_type('expenses', ''):
            # Do they need to revise and resubmit?
            em = ExpenseMonth.objects.filter(
                purchaser=sub, status__in=[
                    ExpenseMonth.STATUS_APPROVER_DENIED,
                    ExpenseMonth.STATUS_DIRECTOR_DENIED,
                    ExpenseMonth.STATUS_FISCAL_DENIED
                ]
            ).exists()
            if em:
                recipients.append(sub.user.email)
    for recipient in recipients:
        html_message = render_to_string(html_template, { 'context': {
            'expenses_url': expenses_url,
            'profile_url': profile_url,
            'from_email': os.environ.get('FROM_EMAIL')
        }, })
        plaintext_message = strip_tags(html_message)
        send_email(
            recipient,
            f'Revise and resubmit expenses',
            plaintext_message,
            html_message
        )
    
    return len(recipients)


# Approver has GLs to approve
# Director has expensemonths to approve
# Fiscal has expensemonths to approve


# Direct notifications
# Approver denied, alert submitter
# Director denied, alert submitter
# Fiscal denied, alert submitter