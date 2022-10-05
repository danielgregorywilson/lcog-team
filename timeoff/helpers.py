from datetime import datetime, time

from django.contrib.sites.models import Site
from django.db.models import Q

from mainsite.helpers import next_weekday, send_email
from people.models import Employee
from timeoff.models import TimeOffRequest


def send_manager_new_timeoff_request_notification(tor):
    current_site = Site.objects.get_current()
    url = current_site.domain + '/timeoff/manage-requests'
    if tor.start_date == tor.end_date:
        message = f'{tor.employee.name} has requested time off on {tor.start_date}. View and acknowledge here: {url}',
    else:
        message = f'{tor.employee.name} has requested time off from {tor.start_date} to {tor.end_date}. View and acknowledge here: {url}',

    send_email(
        tor.employee.manager.user.email,
        f'New time off request: {tor.employee.name}',
        message[0],
        message[0]
    )


def send_employee_manager_acknowledged_timeoff_request_notification(tor):
    current_site = Site.objects.get_current()
    url = current_site.domain + '/timeoff/my-requests'
    employee = tor.employee
    manager_name = employee.manager.name
    
    dates_str = ''
    if tor.start_date == tor.end_date:
        dates_str = f'on {tor.start_date}'
    else:
        dates_str = f'from {tor.start_date} to {tor.end_date}'
    
    if tor.acknowledged:
        message = f'Your manager {manager_name} has acknowledged your time off {dates_str}. View here: {url}',
    else:
        message = f'Your manager {manager_name} has indicated a problem with your time off {dates_str}. View here: {url}',

    send_email(
        employee.user.email,
        f'Time off request response',
        message[0],
        message[0]
    )


def send_is_timeoff_next_week_report():
    current_site = Site.objects.get_current()
    url = current_site.domain + '/timeoff/calendar'
    is_manager = Employee.objects.get(user__username='hleyba')
    is_team = is_manager.get_descendants_of_employee(is_manager)
    tors = TimeOffRequest.objects.filter(employee__in=is_team)
    
    today = datetime.now().date()
    next_monday = next_weekday(today, 0) # 0=Monday, 1=Tuesday, 2=Wednesday...
    next_tuesday = next_weekday(next_monday, 1)
    next_wednesday = next_weekday(next_monday, 2)
    next_thursday = next_weekday(next_monday, 3)
    next_friday = next_weekday(next_monday, 4)
    
    monday_tors = tors.filter(start_date__lte=next_monday, end_date__gte=next_monday)
    tuesday_tors = tors.filter(start_date__lte=next_tuesday, end_date__gte=next_tuesday)
    wednesday_tors = tors.filter(start_date__lte=next_wednesday, end_date__gte=next_wednesday)
    thursday_tors = tors.filter(start_date__lte=next_thursday, end_date__gte=next_thursday)
    friday_tors = tors.filter(start_date__lte=next_friday, end_date__gte=next_friday)

    num_tors = sum([
        monday_tors.count(), tuesday_tors.count(), wednesday_tors.count(),
        thursday_tors.count(), friday_tors.count()
    ])

    if num_tors == 0:
        return num_tors, len(is_team)

    message = 'IS Team\n'
    message += 'Who is out next week:\n'
    message += f'\nMonday {next_monday.strftime("%B %-d")}:\n'
    for tor in monday_tors:
        message += f'{tor.employee.name}\n'
    message += f'\nTuesday {next_tuesday.strftime("%B %-d")}:\n'
    for tor in tuesday_tors:
        message += f'{tor.employee.name}\n'
    message += f'\nWednesday {next_wednesday.strftime("%B %-d")}:\n'
    for tor in wednesday_tors:
        message += f'{tor.employee.name}\n'
    message += f'\nThursday {next_thursday.strftime("%B %-d")}:\n'
    for tor in thursday_tors:
        message += f'{tor.employee.name}\n'
    message += f'\nFriday {next_friday.strftime("%B %-d")}:\n'
    for tor in friday_tors:
        message += f'{tor.employee.name}\n'
    message += f'\nView the full calendar: {url}'

    for recipient in is_team:
        send_email(
            recipient.user.email,
            f'IS Team Time Off Next Week: {next_monday.strftime("%A %B %-d")} - {next_friday.strftime("%A %B %-d, %Y")}',
            message,
            message
        )
    
    return num_tors, len(is_team)


def send_team_timeoff_next_week_report(manager_username: str, team_name: str):
    current_site = Site.objects.get_current()
    url = current_site.domain + '/timeoff/calendar'
    manager = Employee.objects.get(user__username=manager_username)
    team = manager.get_descendants_of_employee(manager)
    tors = TimeOffRequest.objects.filter(employee__in=team)
    
    today = datetime.now().date()
    next_monday = next_weekday(today, 0) # 0=Monday, 1=Tuesday, 2=Wednesday...
    next_tuesday = next_weekday(next_monday, 1)
    next_wednesday = next_weekday(next_monday, 2)
    next_thursday = next_weekday(next_monday, 3)
    next_friday = next_weekday(next_monday, 4)
    
    monday_tors = tors.filter(start_date__lte=next_monday, end_date__gte=next_monday)
    tuesday_tors = tors.filter(start_date__lte=next_tuesday, end_date__gte=next_tuesday)
    wednesday_tors = tors.filter(start_date__lte=next_wednesday, end_date__gte=next_wednesday)
    thursday_tors = tors.filter(start_date__lte=next_thursday, end_date__gte=next_thursday)
    friday_tors = tors.filter(start_date__lte=next_friday, end_date__gte=next_friday)

    num_tors = sum([
        monday_tors.count(), tuesday_tors.count(), wednesday_tors.count(),
        thursday_tors.count(), friday_tors.count()
    ])

    if num_tors == 0:
        return num_tors, len(team)

    plain_message = f'{team_name}\n'
    plain_message += 'Who is out next week:\n'
    plain_message += f'\nMonday {next_monday:%B} {next_monday.day}:\n'
    for tor in monday_tors:
        plain_message += f'{tor.employee.name}\n'
    plain_message += f'\nTuesday {next_tuesday:%B} {next_tuesday.day}:\n'
    for tor in tuesday_tors:
        plain_message += f'{tor.employee.name}\n'
    plain_message += f'\nWednesday {next_wednesday:%B} {next_wednesday.day}:\n'
    for tor in wednesday_tors:
        plain_message += f'{tor.employee.name}\n'
    plain_message += f'\nThursday {next_thursday:%B} {next_thursday.day}:\n'
    for tor in thursday_tors:
        plain_message += f'{tor.employee.name}\n'
    plain_message += f'\nFriday {next_friday:%B} {next_friday.day}:\n'
    for tor in friday_tors:
        plain_message += f'{tor.employee.name}\n'
    plain_message += f'\nView the full calendar: {url}'

    message = f'<h1>{team_name}</h1>'
    message += '<div>Who is out next week:</div>'
    message += f'\nMonday {next_monday:%B} {next_monday.day}:\n'
    for tor in monday_tors:
        message += f'{tor.employee.name}\n'
    message += f'\nTuesday {next_tuesday:%B} {next_tuesday.day}:\n'
    for tor in tuesday_tors:
        message += f'{tor.employee.name}\n'
    message += f'\nWednesday {next_wednesday:%B} {next_wednesday.day}:\n'
    for tor in wednesday_tors:
        message += f'{tor.employee.name}\n'
    message += f'\nThursday {next_thursday:%B} {next_thursday.day}:\n'
    for tor in thursday_tors:
        message += f'{tor.employee.name}\n'
    message += f'\nFriday {next_friday:%B} {next_friday.day}:\n'
    for tor in friday_tors:
        message += f'{tor.employee.name}\n'
    message += f'\nView the full calendar: {url}'

    for recipient in team:
        send_email(
            recipient.user.email,
            f'{team_name} Time Off Next Week: {next_monday:%A} {next_monday:%B} {next_monday.day} - {next_friday:%A} {next_friday:%B} {next_friday.day}, {next_friday.year}',
            plain_message,
            message
        )
    
    return num_tors, len(team)

def send_test_timeoff_next_week_report():
    return send_team_timeoff_next_week_report('programmanager', 'Test Unit')