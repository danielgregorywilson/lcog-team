from django.contrib import admin

from .models import (
    Division, Employee, JobTitle, PerformanceReview,
    ReviewNote, Signature, SignatureReminder,
    TeleworkApplication, TeleworkSignature, UnitOrProgram,
    ViewedSecurityMessage
)
from mainsite.admin import EditLinkToInlineObject


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
    list_display = ("number", "username", "job_title", "unit_or_program", "manager",)
    list_filter = ("active", "unit_or_program__division", "unit_or_program",)
    search_fields = ("user__username", )


# class SelfEvaluationInline(EditLinkToInlineObject, admin.StackedInline):
#     model = EmployeeSelfEvaluation
#     readonly_fields = ('edit_link',)
#     extra = 0


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
    search_fields = ("employee__user__username", )
    inlines = (SignatureInline, SignatureReminderInline)
    # inlines = (SignatureInline, SignatureReminderInline, SelfEvaluationInline)

    def get_form(self, request, obj=None, **kwargs):
        pr_exists = hasattr(obj, 'pk')
        user_is_superuser = request.user.is_superuser
        employee_cannot_view_pr = not hasattr(request.user, 'employee') or obj.pk not in request.user.employee.prs_can_view()
        if pr_exists and not user_is_superuser and employee_cannot_view_pr:
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


# class SelfEvaluationSignatureInline(admin.TabularInline):
#     model = SelfEvaluationSignature
#     extra = 0


# class SelfEvaluationSignatureReminderInline(admin.TabularInline):
#     model = SelfEvaluationSignatureReminder
#     extra = 0


# @admin.register(EmployeeSelfEvaluation)
# class SelfEvaluationAdmin(admin.ModelAdmin):
#     model = EmployeeSelfEvaluation
#     inlines = (SelfEvaluationSignatureInline, SelfEvaluationSignatureReminderInline)


@admin.register(ReviewNote)
class ReviewNoteAdmin(admin.ModelAdmin):
    list_display = ("manager", "employee", "date")
    readonly_fields = ("date",)

    def get_form(self, request, obj=None, **kwargs):
        note_exists = hasattr(obj, 'pk')
        user_is_superuser = request.user.is_superuser
        employee_cannot_view_note = not hasattr(request.user, 'employee') or obj.pk not in request.user.employee.notes_can_view()
        if note_exists and not user_is_superuser and employee_cannot_view_note:
            self.exclude = ('note',)
        else:
            self.exclude = ()
        form = super(ReviewNoteAdmin, self).get_form(request, obj, **kwargs)
        return form


@admin.register(ViewedSecurityMessage)
class ViewedSecurityMessageAdmin(admin.ModelAdmin):
    list_display = ("employee", "security_message", "datetime")


class TeleworkSignatureInline(admin.TabularInline):
    model = TeleworkSignature
    fields = ("employee", "index", "date",)
    readonly_fields = ("date",)
    extra = 0


@admin.register(TeleworkApplication)
class TeleworkApplicationAdmin(admin.ModelAdmin):
    list_display = ("username", "status")
    inlines = (TeleworkSignatureInline,)
