from django.core.management.base import BaseCommand

from timeoff.helpers import send_is_timeoff_next_week_report

class Command(BaseCommand):
    help = 'Sends next week time off email to members of the IS team'

    def handle(self, *args, **options):
        send_is_timeoff_next_week_report()
        # TODO: Output some data about how many emails sent, etc.
        self.stdout.write(self.style.SUCCESS('Sent some emails.'))