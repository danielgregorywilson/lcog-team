from datetime import datetime

from django.core.management.base import BaseCommand

from workflows.helpers import send_employee_transition_report


class Command(BaseCommand):
    help = 'Sends next week time off email to members of the IS team'

    def handle(self, *args, **options):
        num_employees = send_employee_transition_report()
        dt = datetime.now()
        message = f'{dt} - Sent current employee transitions notification ' + \
            f'to {num_employees} managers.'
        self.stdout.write(self.style.SUCCESS(message))