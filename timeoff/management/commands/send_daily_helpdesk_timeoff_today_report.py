from datetime import datetime

from django.core.management.base import BaseCommand

from timeoff.helpers import send_daily_helpdesk_timeoff_today_report


class Command(BaseCommand):
    help = 'Sends today time off email to members of the help desk'

    def handle(self, *args, **options):
        num_tor_days, num_employees = send_daily_helpdesk_timeoff_today_report()
        dt = datetime.now()
        if num_tor_days == 0:
            message = f'{dt} - No time off notifications sent to the help desk.'
        else:
            message = f'{dt} - Sent notification of {num_tor_days} time off requests to {num_employees} help desk employees.'
        self.stdout.write(self.style.SUCCESS(message))