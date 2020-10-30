from django.contrib import admin

from .models import (
    Division, Employee, JobTitle, PerformanceReview, ReviewNote, Signature,
    UnitOrProgram
)


class UnitOrProgramInline(admin.TabularInline):
    model = UnitOrProgram
    extra = 0


@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = (UnitOrProgramInline,)


@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("username", "job_title", "unit_or_program", "manager",)


class SignatureInline(admin.TabularInline):
    model = Signature
    fields = ("employee", "date",)
    readonly_fields = ("date",)
    extra = 0


@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ("username", "period_end_date")
    inlines = (SignatureInline,)


@admin.register(ReviewNote)
class ReviewNoteAdmin(admin.ModelAdmin):
    list_display = ("manager", "employee", "date")
    readonly_fields = ("date",)