from django.core.management.base import BaseCommand, CommandError

from mainsite.helpers import send_pr_reminder_emails

class Command(BaseCommand):
    help = 'Sends reminder emails for in-progress performance reviews'

    def handle(self, *args, **options):
        send_pr_reminder_emails()
        # TODO: Output some data about how many emails sent, etc.
        self.stdout.write(self.style.SUCCESS('Sent some emails.'))
        # self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))sen