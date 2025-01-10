from datetime import datetime

from django.core.management.base import BaseCommand

from purchases.helpers import send_submitter_monthly_expenses_reminders


class Command(BaseCommand):
    help = 'Sends end-of-month email to expense submitters'

    def handle(self, *args, **options):
        num_employees = send_submitter_monthly_expenses_reminders()
        dt = datetime.now()
        message = f'{dt} - Sent end-of-month CC expense notifications to ' + \
            f'{num_employees} submitters.'
        self.stdout.write(self.style.SUCCESS(message))