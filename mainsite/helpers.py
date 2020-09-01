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

def send_evaluation_complete_email(to_addresses, review, host):
    url = host + reverse('performancereview-approval-view', args=[review.pk])
    send_email(
        to_addresses,
        f'A Performance Evaluation is complete and requires your feedback',
        f'A review meeting between {review.employee.user.get_full_name()} and {review.employee.manager.user.get_full_name()} took place on {review.performanceevaluation.discussion_date}. Please review it here: {url}',
        f'A review meeting between {review.employee.user.get_full_name()} and {review.employee.manager.user.get_full_name()} took place on {review.performanceevaluation.discussion_date}. Please review it here: <a href="{url}">{url}</a>',
    )
