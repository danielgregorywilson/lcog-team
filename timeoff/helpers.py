from django.contrib.sites.models import Site

from mainsite.helpers import send_email


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