from django.contrib import admin
from django.forms import BaseInlineFormSet, ModelForm
from django.utils.safestring import mark_safe
from django.urls import reverse

from workflows.models import (
    Action, Process, ProcessInstance, Role, Step, StepChoice, StepInstance,
    Workflow, WorkflowInstance
)


@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    list_display = ("name", "version")


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "members_list")
    filter_horizontal = ("members",)
    
    # Avoid many queries when getting members to display in list
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('members')

    def members_list(self, obj):
        return ",\n".join([employee.name for employee in obj.members.all()])


class GetParentFormSet(BaseInlineFormSet):
    """
    Used to access the parent model instance in an inline model form
    """
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['parent_object'] = self.instance
        return kwargs


class StepForm(ModelForm):
    """Used in Step Admin for next_step"""
    def __init__(self, *args, **kwargs):
        super(StepForm, self).__init__(*args, **kwargs)
        self.fields['next_step'].queryset = Step.objects.filter(process=self.instance.process).exclude(pk=self.instance.pk).order_by('order')


class StepInlineForm(ModelForm):
    """Used in Process Admin for child Steps' next_steps"""
    def __init__(self, *args, parent_object, **kwargs):
        super(StepInlineForm, self).__init__(*args, **kwargs)
        self.fields['next_step'].queryset = Step.objects.filter(process=parent_object).exclude(pk=self.instance.pk).order_by('order')


class StepChoiceForm(ModelForm):
    """Used in Step Admin for Step choices"""
    def __init__(self, *args, parent_object, **kwargs):
        super(StepChoiceForm, self).__init__(*args, **kwargs)
        self.fields['next_step'].queryset = Step.objects.filter(process=parent_object.process).exclude(pk=parent_object.pk).order_by('order')         


class StepInline(admin.TabularInline):
    model = Step
    formset = GetParentFormSet
    form = StepInlineForm
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
    list_display = ("name", "workflow", "version")
    list_filter = ("workflow",)
    inlines = (StepInline,)


class StepChoiceInline(admin.TabularInline):
    model = StepChoice
    formset = GetParentFormSet
    form = StepChoiceForm
    fk_name = "step"
    ordering = ('order',)
    extra = 0


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("process",)
    form = StepForm
    inlines = (StepChoiceInline,)


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ("name", "type")


@admin.register(WorkflowInstance)
class WorkflowInstanceAdmin(admin.ModelAdmin):
    pass


@admin.register(ProcessInstance)
class ProcessInstanceAdmin(admin.ModelAdmin):
    pass


@admin.register(StepInstance)
class StepInstanceAdmin(admin.ModelAdmin):
    pass
