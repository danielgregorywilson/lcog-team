from contextlib import redirect_stdout

from django.core.management.base import BaseCommand

from workflows.models import EmployeeTransition


class Command(BaseCommand):
    help = 'Exports the to-be-deleted Prox Card Returned checkbox'

    def handle(self, *args, **options):
        data = []
        for t in EmployeeTransition.objects.filter(
            type=EmployeeTransition.TRANSITION_TYPE_EXIT
        ):
            data.append({
                'pk': t.pk,
                'employee': f'{t.employee_first_name} {t.employee_last_name}',
                'transition_type': t.type,
                'transition_date': t.transition_date,
                'prox_card_returned': t.prox_card_returned,
            })
        with open('prox-cards.txt', 'w') as f:
            with redirect_stdout(f):
                print(data)