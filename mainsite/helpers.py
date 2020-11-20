import datetime

from django.apps import apps
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.urls import reverse


SEND_MANAGER_FIRST_REMINDER_NEW_PR_DAYS_BEFORE = 60
SEND_MANAGER_SECOND_REMINDER_NEW_PR_DAYS_BEFORE = 45
SEND_MANAGER_PERSISTENT_REMINDERS_NEW_PR_DAYS_BEFORE = 30

EMPLOYEE_SIGNATURE_REMINDER = 2
MANAGER_SIGNATURE_REMINDER = 2
MANAGER_SIGNATURE_REMINDER_SUBSEQUENT = 1

ESCALATION_TO_NEXT_MANAGER_REMINDER = 7


def get_host_url(request):
    host = request.get_host()
    if request.is_secure():
        return f'https://{ host }/'
    else:
        return f'http://{ host }/' 


def send_email(to_address, subject, body, html_body):
    return send_mail(subject, body, 'dwilson@lcog.org', [to_address], html_message=html_body)


def send_evaluation_written_email_to_employee(employee, review):
    # Notification #5
    SignatureReminder = apps.get_model('people.SignatureReminder')
    current_site = Site.objects.get_current()
    url = current_site.domain + '/dashboard'
    send_email(
        employee.user.email,
        f'Signature required: {review.employee.manager.user.get_full_name()} has completed your performance evaluation',
        f'Your manager {review.employee.manager.user.get_full_name()} has completed your evaluation for an upcoming performance review, which requires your signature. View and sign here: {url}',
        f'Your manager {review.employee.manager.user.get_full_name()} has completed your evaluation for an upcoming performance review, which requires your signature. View and sign here: {url}'
    )
    next_reminder = datetime.datetime.today() + datetime.timedelta(days=EMPLOYEE_SIGNATURE_REMINDER)
    SignatureReminder.objects.create(review=review, employee=employee, next_date=next_reminder)


def send_signature_email_to_manager(employee, review):
    # Notification #10
    SignatureReminder = apps.get_model('people.SignatureReminder')
    current_site = Site.objects.get_current()
    url = current_site.domain + '/pr/' + str(review.pk)
    send_email(
        employee.user.email,
        f'Signature required: Performance evaluation for {review.employee.user.get_full_name()}',
        f'{review.employee.manager.user.get_full_name()} has completed an evaluation for {review.employee.user.get_full_name()}, which requires your signature. View and sign here: {url}',
        f'{review.employee.manager.user.get_full_name()} has completed an evaluation for {review.employee.user.get_full_name()}, which requires your signature. View and sign here: {url}'
    )
    next_reminder = datetime.datetime.today() + datetime.timedelta(days=MANAGER_SIGNATURE_REMINDER)
    SignatureReminder.objects.create(review=review, employee=employee, next_date=next_reminder)


def send_signature_email_to_hr_manager(review):
    # Notification #13
    hr_manager = apps.get_model('people.Employee').objects.get(is_hr_manager=True)
    send_signature_email_to_manager(hr_manager, review)


def send_signature_email_to_executive_director(review):
    # Notification #16
    executive_director = apps.get_model('people.Employee').objects.get(is_executive_director=True)
    send_signature_email_to_manager(executive_director, review)


def send_completed_email_to_hr_manager(review):
    # Notification #19
    hr_manager = apps.get_model('people.Employee').objects.get(is_hr_manager=True)
    executive_director = apps.get_model('people.Employee').objects.get(is_executive_director=True)
    current_site = Site.objects.get_current()
    url = current_site.domain + '/print/pr/' + str(review.pk)
    send_email(
        hr_manager.user.email,
        f'A Performance Evaluation has been completed',
        f'{executive_director.user.get_full_name()} has approved a performance evaluation for {review.employee.user.get_full_name()}. Please print it here: {url}',
        f'{executive_director.user.get_full_name()} has approved a performance evaluation for {review.employee.user.get_full_name()}. Please print it here: {url}'
    )


def send_pr_reminder_emails():
    current_site = Site.objects.get_current()
    PerformanceReview = apps.get_model('people.PerformanceReview')
    Signature = apps.get_model('people.Signature')
    SignatureReminder = apps.get_model('people.SignatureReminder')
    today = datetime.date.today()

    users = {}
    notifications = {
        'review_to_write': [], 'review_to_write_other': [],
        'signature_required': [], 'signature_required_other': []
    }
    
    def add_reminder(email, notification_type, subject, text_body, html_body):
        if not email in users.keys():
            users[email] = {
                'review_to_write': [], 'review_to_write_other': [],
                'signature_required': [], 'signature_required_other': []
            }
        users[email][notification_type].append([subject, text_body, html_body])
    
    # Reminders to get a manager to write an evaluation
    for pr in PerformanceReview.objects.filter(status=PerformanceReview.NEEDS_EVALUATION):
        days_until_due = pr.days_until_due()
        if days_until_due in [60, 45]:
            url = current_site.domain + '/pr/' + str(pr.pk)
            # Notification #1
            # Notification #2
            add_reminder(pr.employee.manager.user.email, 'review_to_write', 'Upcoming performance review', f'A review for {pr.employee.user.get_full_name()} is due in {pr.days_until_due()} days on {pr.effective_date}. Write an evaluation here: {url}', f'A review for {pr.employee.user.get_full_name()} is due in {pr.days_until_due()} days on {pr.effective_date}. Write an evaluation here: <a href="{url}">{url}</a>')
        if days_until_due <= 30:
            url = current_site.domain + '/pr/' + str(pr.pk)
            # Notification #3
            add_reminder(pr.employee.manager.user.email, 'review_to_write', 'Performance review behind schedule', f'A review for {pr.employee.user.get_full_name()} is due in {pr.days_until_due()} days on {pr.effective_date}. Write an evaluation here: {url}', f'A review for {pr.employee.user.get_full_name()} is due in {pr.days_until_due()} days on {pr.effective_date}. Write an evaluation here: <a href="{url}">{url}</a>')
            # Notification #4: Reminder to manager's manager
            add_reminder(pr.employee.manager.manager.user.email, 'review_to_write_other', 'Performance review behind schedule', f'A review for {pr.employee.user.get_full_name()} is due from {pr.employee.manager.user.get_full_name()} in {pr.days_until_due()} days on {pr.effective_date}. Contact them here: {pr.employee.manager.user.email}', f'A review for {pr.employee.user.get_full_name()} is due from {pr.employee.manager.user.get_full_name()} in {pr.days_until_due()} days on {pr.effective_date}. Contact them here: {pr.employee.manager.user.email}')
    
    # Reminders to get an employee to sign their own evaluation
    for pr in PerformanceReview.objects.filter(status=PerformanceReview.EVALUATION_WRITTEN):
        # Reminder to employee
        reminder = SignatureReminder.objects.filter(review=pr, employee=pr.employee).latest()
        if reminder.count():
            if today >= reminder.next_date:
                url = current_site.domain + '/pr/' + str(pr.pk)
                employee = pr.employee
                # Notification #6: Remind employee a subsequent time to sign own evaluation
                add_reminder(employee.user.email, 'signature_required', f'Signature required: {employee.manager.user.get_full_name()} has completed your performance evaluation', f'Your manager {employee.manager.user.get_full_name()} has completed your evaluation for an upcoming performance review, which requires your signature. View and sign here: {url}', f'Your manager {employee.manager.user.get_full_name()} has completed your evaluation for an upcoming performance review, which requires your signature. View and sign here: {url}')
                next_reminder = datetime.datetime.today() + datetime.timedelta(days=EMPLOYEE_SIGNATURE_REMINDER)
                SignatureReminder.objects.create(review=pr, employee=employee, next_date=next_reminder)
        else:
            # Notification #6
            add_reminder(employee.user.email, 'signature_required', f'Signature required: {employee.manager.user.get_full_name()} has completed your performance evaluation', f'Your manager {employee.manager.user.get_full_name()} has completed your evaluation for an upcoming performance review, which requires your signature. View and sign here: {url}', f'Your manager {employee.manager.user.get_full_name()} has completed your evaluation for an upcoming performance review, which requires your signature. View and sign here: {url}')
            next_reminder = datetime.datetime.today() + datetime.timedelta(days=EMPLOYEE_SIGNATURE_REMINDER)
            SignatureReminder.objects.create(review=pr, employee=employee, next_date=next_reminder)
        
        # Reminder to their manager
        if reminder.count():
            if today >= reminder.date + ESCALATION_TO_NEXT_MANAGER_REMINDER:
                url = current_site.domain + '/pr/' + str(pr.pk)
                employee = pr.employee
                # Notification #7: Escalate to employee's manager to get employee to sign their evaluation
                add_reminder(employee.manager.user.email, 'signature_required_other', f'A performance review is behind schedule', f'A signature is required by {employee.user.get_full_name()} for their evaluation. Contact them here: {employee.user.email}', f'A signature is required by {employee.user.get_full_name()} for their evaluation. Contact them here: {employee.user.email}')
                # We don't need to make another reminder because this same reminder will trigger every subsequent day
        else:
            # Notification #7: Escalate to employee's manager to get employee to sign their evaluation
            add_reminder(employee.manager.user.email, 'signature_required_other', f'A performance review is behind schedule', f'A signature is required by {employee.user.get_full_name()} for their evaluation. Contact them here: {employee.user.email}', f'A signature is required by {employee.user.get_full_name()} for their evaluation. Contact them here: {employee.user.email}')
            # We don't need to make another reminder because this same reminder will trigger every subsequent day
    

    
    # for pr in PerformanceReview.objects.filter(status=PerformanceReview.EVALUATION_WRITTEN):
    #     # Reminders to get managers to review and sign a written performance evaluation
    #     # Who needs to sign it, when were they last reminded, and then send it to them or their manager if needed
    #     employee = pr.employee.manager
    #     while True:
    #         signatures = Signature.objects.filter(review=pr, employee=employee)
    #         if signatures.count() > 0:
    #             if employee.manager:
    #                 employee = employee.manager
    #             else:
    #                 employee = None
    #         else:
    #             break
    #     reminders = SignatureReminder.objects.filter(review=pr, employee=employee)
    #     if reminders.count() > 0:
    #         #check and maybe send
    #         import pdb; pdb.set_trace()
    #         if today >= reminders[0].next_date: # If it's time to send another reminder
    #             url = current_site.domain + '/pr/' + str(pr.pk)
    #             # Notification #8
    #             add_reminder(employee.user.email, 'signature_required', f'Signature required: Performance evaluation for {pr.employee.user.get_full_name()}', f'{pr.employee.manager.user.get_full_name()} has completed an evaluation for {pr.employee.user.get_full_name()}, which requires your signature. View and sign here: {url}', f'{pr.employee.manager.user.get_full_name()} has completed an evaluation for {pr.employee.user.get_full_name()}, which requires your signature. View and sign here: {url}')
    #             next_reminder = datetime.datetime.today() + datetime.timedelta(days=MANAGER_SIGNATURE_REMINDER)
    #             SignatureReminder.objects.create(review=pr, employee=employee, next_date=next_reminder)
    #             # add_reminder(employee.manager.user.email, 'signature_required_other', f'A performance review is behind schedule', f'A signature is required by {employee.user.get_full_name()} for an evaluation for {pr.employee.user.get_full_name()}. Contact them here: {employee.user.email}', f'A signature is required by {employee.user.get_full_name()} for an evaluation for {pr.employee.user.get_full_name()}. Contact them here: {employee.user.email}')
    #     else:
    #         add_reminder(employee.user.email, 'signature_required', f'Signature required: Performance evaluation for {pr.employee.user.get_full_name()}', f'{pr.employee.manager.user.get_full_name()} has completed an evaluation for {pr.employee.user.get_full_name()}, which requires your signature. View and sign here: {url}', f'{pr.employee.manager.user.get_full_name()} has completed an evaluation for {pr.employee.user.get_full_name()}, which requires your signature. View and sign here: {url}')
    #         SignatureReminder.objects.create(review=pr, employee=employee)
    #         # send

    # Reminders to get the HR manager to review and sign a written performance evaluation

    # Reminders to get the Executive Director to review and sign a written performance evaluation
    for user in users.items():
        print('\n')
        print('USER:', user[0])
        if len(user[1]['review_to_write']):
            print('REVIEW_TO_WRITE')
            for notification in user[1]['review_to_write']:
                print(notification)
        if len(user[1]['review_to_write_other']):
            print('REVIEW_TO_WRITE_OTHER')
            for notification in user[1]['review_to_write_other']:
                print(notification)
        if len(user[1]['signature_required']):
            print('SIGNATURE_REQUIRED')
            for notification in user[1]['signature_required']:
                print(notification)
        if len(user[1]['signature_required_other']):
            print('SIGNATURE_REQUIRED_OTHER')
            for notification in user[1]['signature_required_other']:
                print(notification)
    return


def is_true_string(str):
    if str in ['true', 'True']:
        return True
    return False