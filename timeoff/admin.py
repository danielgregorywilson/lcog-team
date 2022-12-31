from django.contrib import admin

from .models import TimeOffRequest, TimeOffRequestTemporaryApprover


@admin.register(TimeOffRequest)
class TimeOffRequestAdmin(admin.ModelAdmin):
    list_display = ("pk", "employee", "start_date", "end_date", "acknowledged",
        "created_at")


@admin.register(TimeOffRequestTemporaryApprover)
class TimeOffRequestTemporaryApproverAdmin(admin.ModelAdmin):
    list_display = ("employee_on_leave", "employee_in_stead", "start_date",
        "end_date")
