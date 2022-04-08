from django.core.management.base import BaseCommand, CommandError

from deskreservation.helpers import end_all_desk_reservations

class Command(BaseCommand):
    help = 'Ends all active desk reservations. To be run at the end of each day.'

    def handle(self, *args, **options):
        end_all_desk_reservations()
        # TODO: Output some data about how many reservations ended, etc.
        self.stdout.write(self.style.SUCCESS('Ended all active desk reservations.'))