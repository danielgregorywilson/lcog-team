from django.contrib import admin

from .models import (
    Division, Employee, JobTitle, PerformanceReview, ReviewNote, Signature,
    SignatureReminder, UnitOrProgram
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
    list_display = ("name", "position_description_link")


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("username", "job_title", "unit_or_program", "manager",)
    list_filter = ("unit_or_program__division", "unit_or_program",)


class SignatureReminderInline(admin.TabularInline):
    model = SignatureReminder
    fields = ("employee", "date", "next_date")
    readonly_fields = ("date",)
    extra = 0


class SignatureInline(admin.TabularInline):
    model = Signature
    fields = ("employee", "date",)
    readonly_fields = ("date",)
    extra = 0


@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ("username", "status", "effective_date")
    inlines = (SignatureInline, SignatureReminderInline)

    def get_form(self, request, obj=None, **kwargs):
        if hasattr(obj, 'pk') and not request.user.is_superuser and obj.pk not in request.user.employee.prs_can_view():
            self.exclude = (
                'step_increase', 'top_step_bonus', 'action_other',
                'factor_job_knowledge', 'factor_work_quality',
                'factor_work_quantity', 'factor_work_habits',
                'factor_analysis', 'factor_initiative', 'factor_interpersonal',
                'factor_communication', 'factor_dependability',
                'factor_professionalism', 'factor_management',
                'factor_supervision', 'evaluation_successes',
                'evaluation_opportunities', 'evaluation_goals_manager',
                'evaluation_goals_employee', 'evaluation_comments_employee',
                'description_reviewed_employee', 'signed_position_description'
            )
        else:
            self.exclude = ()
        form = super(PerformanceReviewAdmin, self).get_form(request, obj, **kwargs)
        return form


@admin.register(ReviewNote)
class ReviewNoteAdmin(admin.ModelAdmin):
    list_display = ("manager", "employee", "date")
    readonly_fields = ("date",)

    def get_form(self, request, obj=None, **kwargs):
        if hasattr(obj, 'pk') and not request.user.is_superuser and obj.pk not in request.user.employee.notes_can_view():
            self.exclude = ('note',)
        else:
            self.exclude = ()
        form = super(ReviewNoteAdmin, self).get_form(request, obj, **kwargs)
        return form