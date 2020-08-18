from django.contrib import admin

from .models import Employee, PerformanceEvaluation, PerformanceReview

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("username", "manager",)


class PerformanceEvaluationInline(admin.StackedInline):
    model = PerformanceEvaluation
    extra = 0


@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ("username", "date")
    inlines = (PerformanceEvaluationInline,)