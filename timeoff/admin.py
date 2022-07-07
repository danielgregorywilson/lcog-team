from django.contrib import admin

from .models import TimeOffRequest


@admin.register(TimeOffRequest)
class TimeOffRequestAdmin(admin.ModelAdmin):
    list_display = ("pk", "employee", "dates", "acknowledged", "created_at")
