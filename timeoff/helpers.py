from datetime import datetime, time

from django.contrib.sites.models import Site
from django.db.models import Q

from mainsite.helpers import next_weekday, send_email
from people.models import Employee
from timeoff.models import TimeOffRequest


def send_timeoff_request_notification(employee, tor):
    current_site = Site.objects.get_current()
    url = current_site.domain + '/timeoff/manage-requests'
    if tor.start_date == tor.end_date:
        message = f'{tor.employee.user.get_full_name()} has requested time off on {tor.start_date}. View and acknowledge here: {url}',
    else:
        message = f'{tor.employee.user.get_full_name()} has requested time off from {tor.start_date} to {tor.end_date}. View and acknowledge here: {url}',

    send_email(
        employee.user.email,
        f'New time off request: {tor.employee.user.get_full_name()}',
        message[0],
        message[0]
    )


def send_is_timeoff_next_week_report():
    current_site = Site.objects.get_current()
    url = current_site.domain + '/timeoff/calendar'
    is_manager = Employee.objects.get(user__username='hleyba')
    
    today = datetime.now().date()
    next_monday = next_weekday(today, 0) # 0=Monday, 1=Tuesday, 2=Wednesday...
    next_tuesday = next_weekday(next_monday, 1)
    next_wednesday = next_weekday(next_monday, 2)
    next_thursday = next_weekday(next_monday, 3)
    next_friday = next_weekday(next_monday, 4)
    
    tors = TimeOffRequest.objects.filter(
        (
            Q(employee=is_manager) |
            Q(employee__manager=is_manager) |
            Q(employee__manager__manager=is_manager)
        )
    )
    
    monday_tors = tors.filter(start_date__lte=next_monday, end_date__gte=next_monday)
    tuesday_tors = tors.filter(start_date__lte=next_tuesday, end_date__gte=next_tuesday)
    wednesday_tors = tors.filter(start_date__lte=next_wednesday, end_date__gte=next_wednesday)
    thursday_tors = tors.filter(start_date__lte=next_thursday, end_date__gte=next_thursday)
    friday_tors = tors.filter(start_date__lte=next_friday, end_date__gte=next_friday)

    message = 'Who is out next week:\n'
    message += f'\nMonday {next_monday.strftime("%B %-d")}:\n'
    for tor in monday_tors:
        message += f'{tor.employee}\n'
    message += f'\nTuesday {next_tuesday.strftime("%B %-d")}:\n'
    for tor in tuesday_tors:
        message += f'{tor.employee}\n'
    message += f'\nWednesday {next_wednesday.strftime("%B %-d")}:\n'
    for tor in wednesday_tors:
        message += f'{tor.employee}\n'
    message += f'\nThursday {next_thursday.strftime("%B %-d")}:\n'
    for tor in thursday_tors:
        message += f'{tor.employee}\n'
    message += f'\nFriday {next_friday.strftime("%B %-d")}:\n'
    for tor in friday_tors:
        message += f'{tor.employee}\n'

    recipients = Employee.objects.filter(
        Q(pk=is_manager.pk) |
        Q(manager=is_manager) |
        Q(manager__manager=is_manager)
    )

    for recipient in recipients:
        send_email(
            recipient.user.email,
            f'IS Team Time Off Next Week: {next_monday.strftime("%A %B %-d")} - {next_friday.strftime("%A %B %-d, %Y")}',
            message,
            message
        )