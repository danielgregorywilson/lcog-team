from datetime import datetime

from django.core.management.base import BaseCommand, CommandError

from mainsite.helpers import send_pr_reminder_emails


class Command(BaseCommand):
    help = 'Sends reminder emails for in-progress performance reviews'

    def handle(self, *args, **options):
        send_pr_reminder_emails()
        # TODO: Output some data about how many emails sent, etc.
        message = f'{ datetime.now() } - Sent some emails.'
        self.stdout.write(self.style.SUCCESS(message))