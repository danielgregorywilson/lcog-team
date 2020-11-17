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

def send_email(to_addresses, subject, body, html_body):
    return send_mail(subject, body, 'dwilson@lcog.org', to_addresses, html_message=html_body)

def send_evaluation_written_email_to_employee(to_addresses, review):
    current_site = Site.objects.get_current()
    url = current_site.domain + '/dashboard'
    send_email(
        to_addresses,
        f'Signature required: {review.employee.manager.user.get_full_name()} has completed your performance evaluation',
        f'Your manager {review.employee.manager.user.get_full_name()} has completed your evaluation for an upcoming performance review, which requires your signature. View and sign here: {url}',
        f'Your manager {review.employee.manager.user.get_full_name()} has completed your evaluation for an upcoming performance review, which requires your signature. View and sign here: {url}'
    )

def send_signature_email_to_manager(to_addresses, review):
    current_site = Site.objects.get_current()
    url = current_site.domain + '/pr/' + str(review.pk)
    send_email(
        to_addresses,
        f'Signature required: Performance evaluation for {review.employee.user.get_full_name()}',
        f'{review.employee.manager.user.get_full_name()} has completed an evaluation for {review.employee.user.get_full_name()}, which requires your signature. View and sign here: {url}',
        f'{review.employee.manager.user.get_full_name()} has completed an evaluation for {review.employee.user.get_full_name()}, which requires your signature. View and sign here: {url}'
    )

def send_signature_email_to_hr_manager(review):
    hr_manager = apps.get_model('people.Employee').objects.get(is_hr_manager=True)
    send_signature_email_to_manager([hr_manager.user.email], review)

def send_signature_email_to_executive_director(review):
    executive_director = apps.get_model('people.Employee').objects.get(is_executive_director=True)
    send_signature_email_to_manager([executive_director.user.email], review)

def send_completed_email_to_hr_manager(review):
    hr_manager = apps.get_model('people.Employee').objects.get(is_hr_manager=True)
    executive_director = apps.get_model('people.Employee').objects.get(is_executive_director=True)
    current_site = Site.objects.get_current()
    url = current_site.domain + '/print/pr/' + str(review.pk)
    send_email(
        [hr_manager.user.email],
        f'A Performance Evaluation has been completed',
        f'{executive_director.user.get_full_name()} has approved a performance evaluation for {review.employee.user.get_full_name()}. Please print it here: {url}',
        f'{executive_director.user.get_full_name()} has approved a performance evaluation for {review.employee.user.get_full_name()}. Please print it here: {url}'
    )

def is_true_string(str):
    if str in ['true', 'True']:
        return True
    return False