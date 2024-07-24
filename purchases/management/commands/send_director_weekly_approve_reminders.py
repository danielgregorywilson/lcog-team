from datetime import datetime

from django.core.management.base import BaseCommand

from purchases.helpers import send_director_weekly_approve_reminders


class Command(BaseCommand):
    help = 'Sends weekly approve reminder email to division directors'

    def handle(self, *args, **options):
        num_employees = send_director_weekly_approve_reminders()
        dt = datetime.now()
        message = f'{dt} - Sent weekly CC expense notifications to ' + \
            f'{num_employees} directors.'
        self.stdout.write(self.style.SUCCESS(message))