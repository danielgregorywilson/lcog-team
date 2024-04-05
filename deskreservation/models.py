from datetime import datetime

from django.db import models
from django.utils.timezone import get_current_timezone
from django.utils.translation import gettext as _

from mainsite.models import ActiveManager


class Desk(models.Model):
    SCHAEFERS = 'S'
    PARK_PLACE = 'P'
    BUILDING_CHOICE = [
        (SCHAEFERS, 'Schaefers'),
        (PARK_PLACE, 'Park Place')
    ]

    class Meta:
        ordering = ["building", "floor", "number"]

    def __str__(self):
        return f"Desk: {self.get_building_display()} {self.floor}F #{self.number} "

    objects = models.Manager()
    active_objects = ActiveManager()

    building = models.CharField(_("building"), max_length=1, choices=BUILDING_CHOICE, default=SCHAEFERS)
    floor = models.PositiveSmallIntegerField(default=1)
    number = models.CharField(max_length=10, unique=True)
    active = models.BooleanField(default=True)
    lead = models.BooleanField(default=False)
    ergonomic = models.BooleanField(default=False)

    @property
    def held_today(self):
        # Return true if there is a hold on a desk today
        day_of_week = datetime.now(tz=get_current_timezone()).weekday()
        day = None
        if day_of_week == 0:
            day = DeskHold.MONDAY
        elif day_of_week == 1:
            day = DeskHold.TUESDAY
        elif day_of_week == 2:
            day = DeskHold.WEDNESDAY
        elif day_of_week == 3:
            day = DeskHold.THURSDAY
        elif day_of_week == 4:
            day = DeskHold.FRIDAY
        if self.holds.filter(day=day).count():
            return True
        return False
    
    @property
    def todays_hold(self):
        # Return today's hold if there is a hold on a desk today
        day_of_week = datetime.now(tz=get_current_timezone()).weekday()
        if day_of_week == 0:
            day = DeskHold.MONDAY
        elif day_of_week == 1:
            day = DeskHold.TUESDAY
        elif day_of_week == 2:
            day = DeskHold.WEDNESDAY
        elif day_of_week == 3:
            day = DeskHold.THURSDAY
        elif day_of_week == 4:
            day = DeskHold.FRIDAY
        if self.holds.filter(day=day).count():
            return self.holds.filter(day=day).first()
        return None


class DeskHold(models.Model):
    MONDAY = 'M'
    TUESDAY = 'U'
    WEDNESDAY = 'W'
    THURSDAY = 'H'
    FRIDAY = 'F'
    DAY_CHOICE = [
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
    ]

    class Meta:
        unique_together = ["desk", "day"]

    def __str__(self):
        return f"Desk hold for {self.desk} on {self.get_day_display()}s"

    desk = models.ForeignKey("deskreservation.Desk", related_name="holds", on_delete=models.CASCADE)
    employees = models.ManyToManyField("people.Employee", related_name="desk_holds")
    day = models.CharField(_("day"), max_length=1, choices=DAY_CHOICE)


class CurrentlyReservedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(check_out__isnull=True)


class DeskReservation(models.Model):
    class Meta:
        verbose_name = _("Desk Reservation")
        verbose_name_plural = _("Desk Reservations")
        ordering = ["-pk"]
    
    def __str__(self):
        return f"Desk reservation for {self.employee.name}"

    objects = models.Manager()
    currently_reserved_objects = CurrentlyReservedManager()

    employee = models.ForeignKey("people.Employee", related_name="desk_reservations", on_delete=models.CASCADE)
    desk = models.ForeignKey("deskreservation.Desk", related_name="reservations", on_delete=models.CASCADE)
    check_in = models.DateTimeField(_("check-in datetime"), auto_now=False, auto_now_add=True)
    check_out = models.DateTimeField(_("check-out datetime"), null=True, auto_now=False, auto_now_add=False)