import os

from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from mainsite.helpers import readable_date, send_email, send_email_multiple
from people.models import JobTitle
from workflows.models import EmployeeTransition, ProcessInstance

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
    date_string = readable_date(t.transition_date) if t.transition_date else ''

    subject = f'New Gas PIN needed for { name_string }'

    html_template = '../templates/email/employee-transition-gas-pin.html'
    html_message = render_to_string(html_template, {
        'name_string': name_string, 'type_verb': type_verb,
        'date_string': date_string, 'transition_url': transition_url,
        'sender_name': sender_name
    })
    plaintext_message = strip_tags(html_message)

    # Send to Gas PIN admins
    to_users = Group.objects.get(name='Gas PIN Admins').user_set.all()
    to_addresses = [
        user.email for user in to_users if \
        user.employee.should_receive_email_of_type('workflows', 'transitions')
    ]
    send_email_multiple(
        to_addresses, [], subject, plaintext_message, html_message
    )

def send_transition_submitter_email(
    t, extra_message=None, sender_name='', sender_email='', url='',
    reassigned=False
):
    current_site = Site.objects.get_current()
    transition_url = current_site.domain + url
    
    reassigned_subject_string = 'REASSIGNED: ' if reassigned else ''
    title_string = t.title.name if t.title else ''
    if t.type == EmployeeTransition.TRANSITION_TYPE_NEW:
        type_verb = 'starting'
    elif t.type == EmployeeTransition.TRANSITION_TYPE_CHANGE:
        type_verb = 'changing'
    elif t.type == EmployeeTransition.TRANSITION_TYPE_EXIT:
        type_verb = 'terminating'
    else:
        type_verb = 'changing'
    date_string = readable_date(t.transition_date) if t.transition_date else ''

    subject = f'{ reassigned_subject_string }{ title_string } EIS \
        { type_verb } { date_string }'

    html_template = '../templates/email/employee-transition-sds.html'
    html_message = render_to_string(html_template, {
        'title_string': title_string, 'type_verb': type_verb,
        'date_string': date_string, 'extra_message': extra_message,
        'transition_url': transition_url, 'sender_name': sender_name
    })
    plaintext_message = strip_tags(html_message)

    # Send to submitter and copy sender
    to_addresses = [
        t.submitter.user.email if (
            t.submitter and \
            t.submitter.should_receive_email_of_type(
                'workflows', 'transitions'
            ) and t.submitter.user.email
        ) else ''
    ]
    cc_addresses = [sender_email]

    send_email_multiple(
        to_addresses, cc_addresses, subject, plaintext_message, html_message
    )

def send_transition_sds_hiring_leads_email(
    t, extra_message=None, sender_name='', sender_email='', url='',
    reassigned=False
):
    current_site = Site.objects.get_current()
    transition_url = current_site.domain + url
    
    reassigned_subject_string = 'REASSIGNED: ' if reassigned else ''
    title_string = t.title.name if t.title else ''
    if t.type == EmployeeTransition.TRANSITION_TYPE_NEW:
        type_verb = 'starting'
    elif t.type == EmployeeTransition.TRANSITION_TYPE_CHANGE:
        type_verb = 'changing'
    elif t.type == EmployeeTransition.TRANSITION_TYPE_EXIT:
        type_verb = 'terminating'
    else:
        type_verb = 'changing'
    date_string = readable_date(t.transition_date) if t.transition_date else ''

    subject = f'{ reassigned_subject_string }{ title_string } EIS \
        { type_verb } { date_string }'

    html_template = '../templates/email/employee-transition-sds.html'
    html_message = render_to_string(html_template, {
        'title_string': title_string, 'type_verb': type_verb,
        'date_string': date_string, 'extra_message': extra_message,
        'transition_url': transition_url, 'sender_name': sender_name
    })
    plaintext_message = strip_tags(html_message)

    # Send to S&DS hiring leads and copy hiring manager and sender
    to_users = Group.objects.get(name='SDS Hiring Lead').user_set.all()
    to_addresses = [
        user.email for user in to_users if \
        user.employee.should_receive_email_of_type('workflows', 'transitions')
    ]
    cc_addresses = []
    if t.manager and t.manager.user.email:
        cc_addresses.append(t.manager.user.email)
    if sender_email not in cc_addresses:
        cc_addresses.append(sender_email)

    send_email_multiple(
        to_addresses, cc_addresses, subject, plaintext_message, html_message
    )

def send_transition_fiscal_email(
    t, extra_message=None, sender_name='', sender_email='', url='',
    reassigned=False
):
    current_site = Site.objects.get_current()
    transition_url = current_site.domain + url
    
    reassigned_subject_string = 'REASSIGNED: ' if reassigned else ''
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
    date_string = readable_date(t.transition_date) if t.transition_date else ''

    subject = f'{ reassigned_subject_string }{ name_string } EIS { type_verb }\
         { date_string }'

    html_template = '../templates/email/employee-transition-fiscal-hr.html'
    html_message = render_to_string(html_template, {
        'name_string': name_string, 'type_verb': type_verb,
        'date_string': date_string, 'extra_message': extra_message,
        'transition_url': transition_url, 'sender_name': sender_name
    })
    plaintext_message = strip_tags(html_message)

    # Send to fiscal employees and copy hiring manager and tammy/lori
    to_users = Group.objects.get(name='Fiscal Employee').user_set.all()
    to_addresses = [
        user.email for user in to_users if \
        user.employee.should_receive_email_of_type('workflows', 'transitions')
    ]
    cc_addresses = []
    if t.manager and t.manager.user.email:
        cc_addresses.append(t.manager.user.email)
    sds_hiring_leads_users = Group.objects.get(
        name='SDS Hiring Lead'
    ).user_set.all()
    sds_hiring_leads_emails = [
        user.email for user in sds_hiring_leads_users if \
        user.employee.should_receive_email_of_type('workflows', 'transitions')
    ]
    for email in sds_hiring_leads_emails:
        cc_addresses.append(email)

    send_email_multiple(
        to_addresses, cc_addresses, subject, plaintext_message, html_message
    )

def send_early_hr_email(t, url=''):
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
    date_string = readable_date(t.transition_date) if t.transition_date else ''

    subject = (
        f'Just Submitted: { name_string } EIS { type_verb } { date_string }'
    )

    html_template = '../templates/email/employee-transition-fiscal-hr.html'
    html_message = render_to_string(html_template, {
        'name_string': name_string,
        'type_verb': type_verb,
        'date_string': date_string,
        'extra_message': 'This is an early notification to HR. The form has ' +
            'not been approved yet.',
        'transition_url': transition_url,
        'sender_name': ''
    })
    plaintext_message = strip_tags(html_message)

    # Send to HR employees
    to_users = Group.objects.get(name='HR Employee').user_set.all()
    to_addresses = [
        user.email for user in to_users if \
        user.employee.should_receive_email_of_type('workflows', 'transitions')
    ]
    cc_addresses = []

    send_email_multiple(
        to_addresses, cc_addresses, subject, plaintext_message, html_message
    )

def send_transition_hr_email(
    t, extra_message=None, sender_name='', sender_email='', url='',
    reassigned=False
):
    current_site = Site.objects.get_current()
    transition_url = current_site.domain + url
    
    reassigned_subject_string = 'REASSIGNED: ' if reassigned else ''
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
    date_string = readable_date(t.transition_date) if t.transition_date else ''

    subject = f'{ reassigned_subject_string }{ name_string } EIS { type_verb }\
         { date_string }'

    html_template = '../templates/email/employee-transition-fiscal-hr.html'
    html_message = render_to_string(html_template, {
        'name_string': name_string, 'type_verb': type_verb,
        'date_string': date_string, 'extra_message': extra_message,
        'transition_url': transition_url, 'sender_name': sender_name
    })
    plaintext_message = strip_tags(html_message)

    # Send to HR employees and copy hiring manager and fiscal employees
    to_users = Group.objects.get(name='HR Employee').user_set.all()
    to_addresses = [
        user.email for user in to_users if \
        user.employee.should_receive_email_of_type('workflows', 'transitions')
    ]
    cc_addresses = []
    if t.manager and t.manager.user.email:
        cc_addresses.append(t.manager.user.email)
    fiscal_users = Group.objects.get(name='Fiscal Employee').user_set.all()
    fiscal_addresses = [
        user.email for user in fiscal_users if \
        user.employee.should_receive_email_of_type('workflows', 'transitions')
    ]
    for email in fiscal_addresses:
        cc_addresses.append(email)

    send_email_multiple(
        to_addresses, cc_addresses, subject, plaintext_message, html_message
    )

def send_transition_stn_email(
        t, update=False, extra_message=None, sender_name='', url='',
        reassigned=False
    ):
    current_site = Site.objects.get_current()
    transition_url = current_site.domain + url
    
    updated_subject_string = 'UPDATED: ' if update else ''
    reassigned_subject_string = 'REASSIGNED: ' if reassigned else ''
    first_name = t.employee_first_name if t.employee_first_name else ''
    last_name = t.employee_last_name if t.employee_last_name else ''
    name_string = f'{ first_name } { last_name }'
    exit_subject_string = 'EXIT: ' if \
        t.type == EmployeeTransition.TRANSITION_TYPE_EXIT else ''
    date_string = readable_date(t.transition_date) if t.transition_date else ''

    subject = f'{ reassigned_subject_string }{ updated_subject_string }\
        { name_string } { exit_subject_string }EIS { date_string }'
    
    updated_body_string = 'updated ' if update else ''
    exit_body_string = 'Exit ' if \
        t.type == EmployeeTransition.TRANSITION_TYPE_EXIT else ''
    title_name = JobTitle.objects.get(pk=t.title_id).name if t.title_id else ''
    title_string = f'{ title_name}'
    type_body_description = '. Their last day was' if \
        t.type == EmployeeTransition.TRANSITION_TYPE_EXIT else ' starting'

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

def create_process_instances(transition):
    # Create process instances for staff transition workflows. Triggered when
    # a transition form is sent to Staff Transition News.
    onboarding_processes_start = [
        'HR Onboarding', 'HR Onboarding Backgorund Check', 'IS Onboarding',
        'IS Telecom Onboarding', 'SDS Facilities Onboarding', 'SDS Onboarding',
        'SDS Phone Onboarding'
    ]
    returning_processes_start = []
    changing_processes_start = [
        'SDS Phone Changing'
    ]
    exiting_processes_start = []
    wfi = transition.workflowinstance
    # Set the process names based on the transition type
    transition_process_names = onboarding_processes_start
    if (transition.type == EmployeeTransition.TRANSITION_TYPE_RETURN):
        transition_process_names = returning_processes_start
    elif (transition.type == EmployeeTransition.TRANSITION_TYPE_CHANGE):
        transition_process_names = changing_processes_start
    elif (transition.type == EmployeeTransition.TRANSITION_TYPE_EXIT):
        transition_process_names = exiting_processes_start
    # Create process instances for each process in the list
    for process in wfi.workflow.processes.filter(
        name__in=transition_process_names
    ):
        existing_pis = ProcessInstance.objects.filter(
            process=process, workflow_instance=wfi
        )
        if existing_pis.count() == 0:
            process.create_process_instance(wfi)
