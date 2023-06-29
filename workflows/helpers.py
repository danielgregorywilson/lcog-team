import os

from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from mainsite.helpers import send_email, send_email_multiple
from people.models import JobTitle
from workflows.models import EmployeeTransition

STAFF_TRANSITION_NEWS_EMAIL = os.environ.get('STAFF_TRANSITION_NEWS_EMAIL')

def send_gas_pin_notification_email(
    t, sender_name='', sender_email='', url=''
):
    current_site = Site.objects.get_current()
    transition_url = current_site.domain + url

    first_name = t.employee_first_name if t.employee_first_name else ''
    last_name = t.employee_last_name if t.employee_last_name else ''
    name_string = f'{ first_name } { last_name }'
    if t.type == EmployeeTransition.TRANSITION_TYPE_NEW:
        type_verb = 'starting'
    elif t.type == EmployeeTransition.TRANSITION_TYPE_CHANGE:
        type_verb = 'changing'
    elif t.type == EmployeeTransition.TRANSITION_TYPE_EXIT:
        type_verb = 'terminating'
    else:
        type_verb = 'changing'
    date_string = t.transition_date.strftime('%m-%d-%y') if t.transition_date else ''

    subject = f'New Gas PIN needed for { name_string }'

    html_template = '../templates/email/employee-transition-gas-pin.html'
    html_message = render_to_string(html_template, {
        'name_string': name_string, 'type_verb': type_verb,
        'date_string': date_string, 'transition_url': transition_url,
        'sender_name': sender_name
    })
    plaintext_message = strip_tags(html_message)

    # Send to Gas PIN admins
    to_addresses = Group.objects.get(name='Gas PIN Admins').user_set.all().values_list('email', flat=True)

    send_email_multiple(
        to_addresses, [], subject, plaintext_message, html_message
    )

def send_transition_hr_email(
    t, extra_message=None, sender_name='', sender_email='', url=''
):
    current_site = Site.objects.get_current()
    transition_url = current_site.domain + url
    
    first_name = t.employee_first_name if t.employee_first_name else ''
    last_name = t.employee_last_name if t.employee_last_name else ''
    name_string = f'{ first_name } { last_name }'
    if t.type == EmployeeTransition.TRANSITION_TYPE_NEW:
        type_verb = 'starting'
    elif t.type == EmployeeTransition.TRANSITION_TYPE_CHANGE:
        type_verb = 'changing'
    elif t.type == EmployeeTransition.TRANSITION_TYPE_EXIT:
        type_verb = 'terminating'
    else:
        type_verb = 'changing'
    date_string = t.transition_date.strftime('%m-%d-%y') if t.transition_date else ''

    subject = f'{ name_string } EIS { type_verb } { date_string }'

    html_template = '../templates/email/employee-transition-hr.html'
    html_message = render_to_string(html_template, {
        'name_string': name_string, 'type_verb': type_verb,
        'date_string': date_string, 'extra_message': extra_message,
        'transition_url': transition_url, 'sender_name': sender_name
    })
    plaintext_message = strip_tags(html_message)

    # Send to scornelius and ssalladay and copy hiring manager and tammy/lori
    to_addresses = Group.objects.get(name='HR Employee').user_set.all().values_list('email', flat=True)
    cc_addresses = []
    if t.manager and t.manager.user.email:
        cc_addresses.append(t.manager.user.email)
    sds_hiring_leads = Group.objects.get(name='SDS Hiring Lead').user_set.all().values_list('email', flat=True)
    for email in sds_hiring_leads:
        cc_addresses.append(email)

    send_email_multiple(
        to_addresses, cc_addresses, subject, plaintext_message, html_message
    )

def send_transition_stn_email(t, update=False, extra_message=None, sender_name='', url=''):
    current_site = Site.objects.get_current()
    transition_url = current_site.domain + url
    
    updated_subject_string = 'UPDATED: ' if update else ''
    first_name = t.employee_first_name if t.employee_first_name else ''
    last_name = t.employee_last_name if t.employee_last_name else ''
    name_string = f'{ first_name } { last_name }'
    exit_subject_string = 'EXIT: ' if t.type == EmployeeTransition.TRANSITION_TYPE_EXIT else ''
    date_string = t.transition_date.strftime('%m-%d-%y') if t.transition_date else ''

    subject = f'{ updated_subject_string }{ name_string } { exit_subject_string }EIS { date_string }'
    
    updated_body_string = 'updated ' if update else ''
    exit_body_string = 'Exit ' if t.type == EmployeeTransition.TRANSITION_TYPE_EXIT else ''
    title_name = JobTitle.objects.get(pk=t.title_id).name if t.title_id else ''
    title_string = f'{ title_name} '
    type_body_description = 'Their last day was ' if t.type == EmployeeTransition.TRANSITION_TYPE_EXIT else 'starting '

    html_template = '../templates/email/employee-transition-stn.html'
    html_message = render_to_string(html_template, {
        'updated_body_string': updated_body_string,
        'exit_body_string': exit_body_string, 'name_string': name_string,
        'title_string': title_string,
        'type_body_description': type_body_description,
        'date_string': date_string,
        'extra_message': extra_message,
        'transition_url': transition_url, 'sender_name': sender_name
    })
    plaintext_message = strip_tags(html_message)

    send_email(
        STAFF_TRANSITION_NEWS_EMAIL, subject, plaintext_message, html_message
    )
