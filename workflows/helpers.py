import os

from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from mainsite.helpers import send_email
from people.models import JobTitle
from workflows.models import EmployeeTransition

STAFF_TRANSITION_NEWS_EMAIL = os.environ.get('STAFF_TRANSITION_NEWS_EMAIL')

def send_staff_transition_email(t, update=False, extra_message=None, sender_name='', url=''):
    current_site = Site.objects.get_current()
    transition_url = current_site.domain + url
    
    updated_subject_string = 'UPDATED: ' if update else ''
    first_name = t.employee_first_name if t.employee_first_name else ''
    last_name = t.employee_last_name if t.employee_last_name else ''
    name_string = f'{first_name} {last_name}'
    exit_subject_string = 'EXIT: ' if t.type == EmployeeTransition.TRANSITION_TYPE_EXIT else ''
    date_string = t.transition_date.strftime('%m-%d-%y') if t.transition_date else ''

    subject = f'{ updated_subject_string }{ name_string } { exit_subject_string }EIS { date_string }'
    
    updated_body_string = 'updated ' if update else ''
    exit_body_string = 'Exit ' if t.type == EmployeeTransition.TRANSITION_TYPE_EXIT else ''
    title_name = JobTitle.objects.get(pk=t.title_id).name if t.title_id else ''
    title_string = f'{ title_name} '
    type_body_description = 'Their last day was ' if t.type == EmployeeTransition.TRANSITION_TYPE_EXIT else 'starting '

    html_template = '../templates/email/employee-transition.html'
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
        STAFF_TRANSITION_NEWS_EMAIL,
        subject,
        plaintext_message,
        html_message
    )
