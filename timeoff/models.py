from django.db import models


class TimeOffRequest(models.Model):
    employee = models.ForeignKey("people.Employee", on_delete=models.CASCADE)
    dates = models.JSONField(default=list)
    note = models.TextField(blank=True, null=True)
    acknowledged = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    acknowledged_at = models.DateTimeField(blank=True, null=True)
