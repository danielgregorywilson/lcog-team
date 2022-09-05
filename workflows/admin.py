from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse

from workflows.models import Process, Role, Step, StepChoice, Workflow


@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "members_list")
    filter_horizontal = ("members",)
    
    # Avoid many queries when getting members to display in list
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('members')

    def members_list(self, obj):
        return "\n".join([employee.name for employee in obj.members.all()])


class StepInline(admin.TabularInline):
    model = Step
    ordering = ('order',)
    readonly_fields = ("edit_link", "next_step_choices")
    extra = 0

    def edit_link(self, instance):
        url = reverse('admin:%s_%s_change' % (
            instance._meta.app_label,  instance._meta.model_name),  args=[instance.pk] )
        if instance.pk:
            return mark_safe(u'<a href="{u}">edit</a>'.format(u=url))
        else:
            return ''

    def next_step_choices(self, instance):
        choices_text = ''
        for idx, choice in enumerate(instance.next_step_choices.all()):
            if idx != 0:
                choices_text += " / "
            choices_text += choice.choice_text + ": " + choice.next_step.name
        return choices_text


@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    list_display = ("name", "workflow")
    list_filter = ("workflow",)
    inlines = (StepInline,)


class StepChoiceInline(admin.TabularInline):
    model = StepChoice
    fk_name = "step"
    ordering = ('order',)
    extra = 0


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    inlines = (StepChoiceInline,)



