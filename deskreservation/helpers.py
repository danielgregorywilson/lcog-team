from datetime import datetime

from django.apps import apps
from django.utils.timezone import get_current_timezone


def end_all_desk_reservations():
    DeskReservation = apps.get_model('people.DeskReservation')
    active_reservations = DeskReservation.objects.filter(check_out__isnull=True)
    for reservation in active_reservations:
        reservation.check_out = datetime.now(tz=get_current_timezone())
        reservation.save()

