from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from deskreservation.models import Desk, DeskReservation

class Command(BaseCommand):
    help = 'Generate a desk usage report'

    def add_arguments(self, parser):
        parser.add_argument('--start_date', help='Start date (inclusive)')
        parser.add_argument('--end_date', help='End date (inclusive)')

    def handle(self, *args, **options):
        import pdb; pdb.set_trace();
        if options.get('start_date') != None and options.get('end_date') != None:
            start_str = options.get('start_date')
            end_str = options.get('end_date')
        else:
            start_str = input('Enter start date (yyyy-mm-dd, defaults to beginning of last month')
            end_str = input('Enter end date (yyyy-mm-dd, defaults to end of last month')

        import pdb; pdb.set_trace();

        start_date = datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(end_str, '%Y-%m-%d %H:%M:%S')

        
        
        for poll_id in options['poll_ids']:
            try:
                poll = Poll.objects.get(pk=poll_id)
            except Poll.DoesNotExist:
                raise CommandError('Poll "%s" does not exist' % poll_id)

            poll.opened = False
            poll.save()

            self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))