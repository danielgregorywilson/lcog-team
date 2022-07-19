from django.db import models
from django.utils.translation import gettext as _


class TimeOffRequest(models.Model):
    class Meta:
        verbose_name = _("Time Off Request")
        verbose_name_plural = _("Time Off Requests")
        ordering = ordering = ["id"]

    employee = models.ForeignKey("people.Employee", on_delete=models.CASCADE)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    note = models.TextField(blank=True, null=True)
    acknowledged = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    acknowledged_at = models.DateTimeField(blank=True, null=True)
