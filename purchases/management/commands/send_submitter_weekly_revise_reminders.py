from datetime import datetime

from django.core.management.base import BaseCommand

from purchases.helpers import send_submitter_weekly_revise_reminders


class Command(BaseCommand):
    help = 'Sends weekly revise reminder email to expense submitters'

    def handle(self, *args, **options):
        num_employees = send_submitter_weekly_revise_reminders()
        dt = datetime.now()
        message = f'{dt} - Sent weekly CC expense notifications to \
            {num_employees} submitters.'
        self.stdout.write(self.style.SUCCESS(message))