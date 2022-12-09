from datetime import datetime

from django.core.management.base import BaseCommand

from timeoff.helpers import send_is_timeoff_next_week_report


class Command(BaseCommand):
    help = 'Sends next week time off email to members of the IS team'

    def handle(self, *args, **options):
        num_tor_days, num_employees = send_is_timeoff_next_week_report()
        dt = datetime.now()
        if num_tor_days == 0:
            message = f'{dt} - No time off notifications sent to the IS team.'
        else:
            message = f'{dt} - Sent notification of {num_tor_days} time off requests to {num_employees} IS employees.'
        self.stdout.write(self.style.SUCCESS(message))