from django.contrib import admin

from .models import Desk, DeskHold, DeskReservation


class DeskHoldInline(admin.TabularInline):
    model = DeskHold
    extra = 0
    max_num = 5
    fields = ("employees", "day", "dates", "active")
    filter_horizontal = ("employees",)


@admin.register(Desk)
class DeskAdmin(admin.ModelAdmin):
    list_display = ("pk", "active", "building", "floor", "number", "lead", "ergonomic")
    list_filter = ("building", "floor", "lead", "ergonomic")
    inlines = (DeskHoldInline,)


@admin.register(DeskReservation)
class DeskReservationAdmin(admin.ModelAdmin):
    list_display = ("pk", "employee", "desk", "check_in", "check_out")
    search_fields = ("employee__user__username", )
    list_filter = ("desk__building", "desk__floor", "desk__number")
    fields = ("employee", "desk", "check_in", "check_out")
    readonly_fields = ("check_in",)