from django.contrib.sites.models import Site

from mainsite.helpers import send_email
from people.models import JobTitle
from workflows.models import EmployeeTransition

STAFF_TRANSITION_NEWS_EMAIL = 'dwilson@lcog.org'

def send_staff_transition_email(t, update=False, extra_message=None):
    current_site = Site.objects.get_current()
    url = current_site.domain + '/timeoff/manage-requests'
    
    updated_subject_string = 'UPDATED: ' if update else ''
    first_name = t.employee_first_name if t.employee_first_name else ''
    last_name = t.employee_last_name if t.employee_last_name else ''
    name_string = f'{first_name} {last_name}'
    exit_subject_string = 'EXIT: ' if t.type == EmployeeTransition.TRANSITION_TYPE_EXIT else ''
    date_string = t.transition_date if t.transition_date else ''

    subject = f'{ updated_subject_string }{ name_string } { exit_subject_string }EIS { date_string }'
    
    updated_body_string = 'updated ' if update else ''
    exit_body_string = 'Exit ' if t.type == EmployeeTransition.TRANSITION_TYPE_EXIT else ''
    title_name = JobTitle.objects.get(pk=t.title_id).name if t.title_id else ''
    title_string = f'{ title_name} '
    type_body_description = 'Their last day was ' if t.type == EmployeeTransition.TRANSITION_TYPE_EXIT else 'starting '
    extra_message_string = f' { extra_message }' if extra_message else ''

    message = f'Attached is an { updated_body_string }{ exit_body_string }EIS for { name_string }, { title_string } { type_body_description }{ date_string }.{ extra_message_string }'

    send_email(
        STAFF_TRANSITION_NEWS_EMAIL,
        subject,
        message[0],
        message[0]
    )
