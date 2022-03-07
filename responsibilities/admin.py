from django.contrib import admin

from .models import Responsibility


@admin.register(Responsibility)
class ResponsibilityAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "primary_employee", "secondary_employee")


# @admin.register(Responsibility)
class ResponsibilityTagAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "primary_employee", "secondary_employee")
