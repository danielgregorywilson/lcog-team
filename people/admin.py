from django.contrib import admin

from .models import Employee, PerformanceReview, ReviewNote

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("username", "manager",)


@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ("username", "period_end_date")


@admin.register(ReviewNote)
class ReviewNoteAdmin(admin.ModelAdmin):
    list_display = ("manager", "employee", "date")
    readonly_fields = ("date",)