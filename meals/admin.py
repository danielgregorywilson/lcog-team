from django.contrib import admin

from .models import Route, Stop

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    pass

@admin.register(Stop)
class StopAdmin(admin.ModelAdmin):
    list_display = ("pk", "first_name", "last_name", "route", "meal_type", "waitlist")
    list_filter = ("route", "meal_type", "waitlist")
