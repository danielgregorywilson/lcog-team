from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _


class Workflow(models.Model):
    """
    A high-level workflow, e.g. new employee onboarding.
    """
    def __str__(self):
        return f"Workflow: {self.name}"
    
    name = models.CharField(max_length=100)
    version = models.IntegerField(default=1)

    # TODO: Complete when all child processes are complete


class Process(models.Model):
    """
    A process within a workflow with a definite start and end. May be done in
    parallel with one another.
    e.g. HR and IS processes for new employee onboarding
    """
    def __str__(self):
        return f"Process: {self.name}"

    class Meta:
        verbose_name_plural = _("Processes")
    
    name = models.CharField(max_length=100)
    workflow = models.ForeignKey(Workflow, related_name="processes", on_delete=models.CASCADE)
    version = models.IntegerField(default=1)

    #TODO: Complete when step marked "end" is completed


class Role(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    members = models.ManyToManyField("people.Employee", related_name="workflow_roles", blank=True)


class Step(models.Model):
    def __str__(self):
        return self.name

    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    order = models.IntegerField(help_text=_("Display order in admin Process detail"), default=0)
    start = models.BooleanField(default=False)
    end = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    role = models.ForeignKey(Role, blank=True, null=True, on_delete=models.SET_NULL, help_text=_("The set of employees responsible for completing this step"))
    next_step = models.ForeignKey("self",  blank=True, null=True, on_delete=models.SET_NULL, help_text=_("The next step, when there is only one"))
    choices_prompt = models.CharField(max_length=200, blank=True, help_text=_("The prompt for when there are multiple next step choices"))

    # TODO: These checks are not working with StepInline readonly_fields
    # def clean(self):
    #     # A process can only have one start and one end step
    #     if self.start and self.process.step_set.filter(start=True).count() > 1:
    #         raise ValidationError("A process can't have more than one start step.")
    #     if self.end and self.process.step_set.filter(end=True).count() > 1:
    #         raise ValidationError("A process can't have more than one end step.")
        
    #     # TODO: Implement check for infinite loops?
    #     if self.next_step == self:
    #         raise ValidationError("A step can't be its own next step.")

    @property
    def members(self):
        if self.role and self.role.members.count():
            return self.role.members.all()
        else:
            return None

    #TODO: On save, error if no next and not end
    #TODO: Properties for next step, previous step, is first step and is last step


class StepChoice(models.Model):
    step = models.ForeignKey(Step, related_name="next_step_choices", on_delete=models.CASCADE)
    order = models.IntegerField(help_text=_("Display order in admin Step detail"), default=0)
    choice_text = models.CharField(max_length=100)
    next_step = models.ForeignKey(Step, blank=True, null=True, on_delete=models.SET_NULL)


class HasTimeStampsMixin(models.Model):
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    @property
    def duration(self):
        if self.completed_at:
            return self.completed_at - self.started_at
        else:
            return None


class WorkflowInstance(HasTimeStampsMixin):
    class Meta:
        ordering = ["pk"]

    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)

    @property
    def current_step_instance(self):
        import pdb; pdb.set_trace();


class ProcessInstance(HasTimeStampsMixin):
    process = models.ForeignKey("workflows.Process", on_delete=models.CASCADE)
    workflow_instance = models.ForeignKey(WorkflowInstance, on_delete=models.CASCADE)
    current_step_instance = models.ForeignKey("workflows.StepInstance", blank=True, null=True, on_delete=models.SET_NULL)


class StepInstance(HasTimeStampsMixin):
    class Meta:
        ordering = ["pk"]
    
    step = models.ForeignKey(Step, on_delete=models.CASCADE)
    process_instance = models.ForeignKey(ProcessInstance, on_delete=models.CASCADE)
    completed_by = models.ForeignKey("people.Employee", blank=True, null=True, on_delete=models.SET_NULL)

    #TODO: Complete method fills completed_at, completed_by, and current_step_instance and completed_at on Workflow instance
