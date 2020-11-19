from django.apps import apps
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.urls import reverse


def get_host_url(request):
    host = request.get_host()
    if request.is_secure():
        return f'https://{ host }/'
    else:
        return f'http://{ host }/' 

def send_email(to_address, subject, body, html_body):
    return send_mail(subject, body, 'dwilson@lcog.org', [to_address], html_message=html_body)

def send_evaluation_written_email_to_employee(employee, review):
    SignatureReminder = apps.get_model('people.SignatureReminder')
    current_site = Site.objects.get_current()
    url = current_site.domain + '/dashboard'
    send_email(
        employee.user.email,
        f'Signature required: {review.employee.manager.user.get_full_name()} has completed your performance evaluation',
        f'Your manager {review.employee.manager.user.get_full_name()} has completed your evaluation for an upcoming performance review, which requires your signature. View and sign here: {url}',
        f'Your manager {review.employee.manager.user.get_full_name()} has completed your evaluation for an upcoming performance review, which requires your signature. View and sign here: {url}'
    )
    SignatureReminder.objects.create(review=review, employee=employee)

def send_signature_email_to_manager(employee, review):
    SignatureReminder = apps.get_model('people.SignatureReminder')
    current_site = Site.objects.get_current()
    url = current_site.domain + '/pr/' + str(review.pk)
    send_email(
        employee.user.email,
        f'Signature required: Performance evaluation for {review.employee.user.get_full_name()}',
        f'{review.employee.manager.user.get_full_name()} has completed an evaluation for {review.employee.user.get_full_name()}, which requires your signature. View and sign here: {url}',
        f'{review.employee.manager.user.get_full_name()} has completed an evaluation for {review.employee.user.get_full_name()}, which requires your signature. View and sign here: {url}'
    )
    SignatureReminder.objects.create(review=review, employee=employee)

def send_signature_email_to_hr_manager(review):
    hr_manager = apps.get_model('people.Employee').objects.get(is_hr_manager=True)
    send_signature_email_to_manager(hr_manager, review)

def send_signature_email_to_executive_director(review):
    executive_director = apps.get_model('people.Employee').objects.get(is_executive_director=True)
    send_signature_email_to_manager(executive_director, review)

def send_completed_email_to_hr_manager(review):
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

SEND_MANAGER_FIRST_REMINDER_NEW_PR_DAYS_BEFORE = 60
SEND_MANAGER_SECOND_REMINDER_NEW_PR_DAYS_BEFORE = 45
SEND_MANAGER_PERSISTENT_REMINDERS_NEW_PR_DAYS_BEFORE = 30

def send_pr_reminder_emails():
    current_site = Site.objects.get_current()
    PerformanceReview = apps.get_model('people.PerformanceReview')
    Signature = apps.get_model('people.Signature')
    SignatureReminder = apps.get_model('people.SignatureReminder')
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
    
    for pr in PerformanceReview.objects.filter(status=PerformanceReview.NEEDS_EVALUATION):
        # Reminders to get a manager to write an evaluation
        days_until_due = pr.days_until_due()
        if days_until_due in [60, 45]:
            url = current_site.domain + '/pr/' + str(pr.pk)
            add_reminder(pr.employee.manager.user.email, 'review_to_write', 'Upcoming performance review', f'A review for {pr.employee.user.get_full_name()} is due in {pr.days_until_due()} days on {pr.effective_date}. Write an evaluation here: {url}', f'A review for {pr.employee.user.get_full_name()} is due in {pr.days_until_due()} days on {pr.effective_date}. Write an evaluation here: <a href="{url}">{url}</a>')
        if days_until_due <= 30:
            url = current_site.domain + '/pr/' + str(pr.pk)
            add_reminder(pr.employee.manager.user.email, 'review_to_write', 'Performance review behind schedule', f'A review for {pr.employee.user.get_full_name()} is due in {pr.days_until_due()} days on {pr.effective_date}. Write an evaluation here: {url}', f'A review for {pr.employee.user.get_full_name()} is due in {pr.days_until_due()} days on {pr.effective_date}. Write an evaluation here: <a href="{url}">{url}</a>')
            add_reminder(pr.employee.manager.manager.user.email, 'review_to_write_other', 'Performance review behind schedule', f'A review for {pr.employee.user.get_full_name()} is due from {pr.employee.manager.user.get_full_name()} in {pr.days_until_due()} days on {pr.effective_date}. Contact them here: {pr.employee.manager.user.email}', f'A review for {pr.employee.user.get_full_name()} is due from {pr.employee.manager.user.get_full_name()} in {pr.days_until_due()} days on {pr.effective_date}. Contact them here: {pr.employee.manager.user.email}')
    for pr in PerformanceReview.objects.filter(status=PerformanceReview.EVALUATION_WRITTEN):
        # Reminders to get managers to review and sign a written performance evaluation
        # Who needs to sign it, when were they last reminded, and then send it to them or their manager if needed
        employee = pr.employee.manager
        while True:
            signatures = Signature.objects.filter(review=pr, employee=employee)
            if signatures.count() > 0:
                employee = employee.manager
            else:
                break
        reminders = SignatureReminder.objects.filter(review=pr, employee=employee)
        if reminders.count() > 0:
            #check and maybe send
            today = datetime.date.today()
            delta = today - reminders[0].date
            if delta.days > 2:
                pass
                #TODO: We're going to need more granularity about next reminder. We might need to record them all and calculate the next one and store it on current one
        else:
            SignatureReminder.objects.create(review=pr, employee=employee)
            # send

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