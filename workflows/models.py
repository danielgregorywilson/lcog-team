from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _


class Role(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    members = models.ManyToManyField("people.Employee", related_name="workflow_roles", blank=True)


class Workflow(models.Model):
    """
    A high-level workflow, e.g. new employee onboarding.
    """
    class Meta:
        ordering = ["pk"]
    
    def __str__(self):
        return f"Workflow: {self.name}"
    
    name = models.CharField(max_length=100)
    role = models.ForeignKey(Role, blank=True, null=True, on_delete=models.SET_NULL, help_text=_("The set of employees with full admin access to this workflow"))
    version = models.IntegerField(default=1)

    # TODO: Complete when all child processes are complete


class Process(models.Model):
    """
    A process within a workflow with a definite start and end. May be done in
    parallel with one another.
    e.g. HR and IS processes for new employee onboarding
    """
    def __str__(self):
        return f"Process: {self.name} v{self.version}"

    class Meta:
        verbose_name_plural = _("Processes")
    
    name = models.CharField(max_length=100)
    workflow = models.ForeignKey(Workflow, related_name="processes", on_delete=models.CASCADE)
    workflow_start = models.BooleanField(default=False, help_text=_("Start this process when a workflow begins."))
    role = models.ForeignKey(Role, blank=True, null=True, on_delete=models.SET_NULL, help_text=_("The set of employees with full admin access to this process"))
    version = models.IntegerField(default=1)

    @property
    def total_steps(self):
        return 1000
        # TODO

    def create_process_instance(self, wfi):
        pi = ProcessInstance.objects.create(process=self, workflow_instance=wfi)
        first_step = self.step_set.filter(start=True)[0]
        si = StepInstance.objects.create(step=first_step, process_instance=pi)
        pi.current_step_instance = si
        pi.save()

    #TODO: Complete when step marked "end" is completed
    # TODO: On save, make sure there is a start and end step if there are any steps


class Action(models.Model):
    LINK = 'LINK'
    API = 'API'
    EMAIL = 'EMAIL'
    ACTION_TYPE_CHOICES = [
        (LINK, 'Navigate to Link'),
        (API, 'Make API call'),
        (EMAIL, 'Send an email'),
    ]
    
    type = models.CharField(_("action type"), max_length=5, choices=ACTION_TYPE_CHOICES, blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.name

    def clean(self):
        # A link must have a URL
        if self.type == self.LINK and not self.url:
            raise ValidationError("A link must have a URL")
        elif self.type == self.API:
            # TODO
            pass
        elif self.type == self.EMAIL:
            # TODO
            pass


class Step(models.Model):
    def __str__(self):
        return f"{self.order} - {self.name}"

    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    order = models.IntegerField(help_text=_("Display order in admin Process detail"), default=0)
    start = models.BooleanField(default=False)
    end = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    role = models.ForeignKey(Role, blank=True, null=True, on_delete=models.SET_NULL, help_text=_("The set of employees responsible for completing this step"))
    next_step = models.ForeignKey("self",  blank=True, null=True, on_delete=models.SET_NULL, help_text=_("The next step, when there is only one"))
    choices_prompt = models.CharField(max_length=200, blank=True, help_text=_("The prompt for when there are multiple next step choices"))
    trigger_processes = models.ManyToManyField(Process, related_name="triggering_steps", blank=True)
    completion_action = models.ForeignKey(Action, blank=True, null=True, on_delete=models.SET_NULL, help_text=_("Action to trigger as this step completes"))
    optional_actions = models.ManyToManyField(Action, blank=True, related_name="triggering_steps")

    # TODO: On save, make sure there is only one start and end step for a given process

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

    @property
    def num_steps_before(self):
        """
        Count the number of steps before the current step. Since there are
        multiple possible paths to the beginning of a process, just get one
        route back and call that sufficient.
        TODO: Rewrite to calculate the best-case (quickest) path back (or worst
        case, or average of all cases)
        """
        num_steps = 0
        current_step = self
        while True:
            if current_step.start == True:
                # We have reached the beginning of the process.
                break
            else:
                # Here we just get the first previous step we can
                previous_step = Step.objects.filter(next_step=current_step).first()
                if not previous_step:
                    # In the case of a choice, there is no next step, so find
                    # the step that leads to this one with choices.
                    step_choice = StepChoice.objects.filter(next_step=current_step).first()
                    previous_step = step_choice.step
                if not previous_step:
                    raise Exception("Couldn't find a previous step.")
                # Move back one step
                current_step = previous_step
                num_steps += 1
        return num_steps

    @property
    def num_steps_after(self):
        num_steps = 0
        current_step = self.process.step_set.get(start=True)
        while True:
            if current_step == self:
                break
            if current_step.end == True:
                raise Exception("Got to the end of the Process without finding the step")
        return num_steps

    #TODO: On save, error if no next and not end
    #TODO: Properties for next step, previous step, is first step and is last step


class StepChoice(models.Model):
    step = models.ForeignKey(Step, related_name="next_step_choices", on_delete=models.CASCADE)
    order = models.IntegerField(help_text=_("Display order in admin Step detail"), default=0)
    choice_text = models.CharField(max_length=100)
    next_step = models.ForeignKey(Step, blank=True, null=True, on_delete=models.SET_NULL)


class HasTimeStampsMixin(models.Model):
    class Meta:
        abstract = True

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

    # @property
    # def current_step_instance(self):
    #     import pdb; pdb.set_trace();

    @property
    def percent_complete(self):
        pis = self.processinstance_set.all()
        total_steps = sum([pi.total_steps for pi in pis])
        if total_steps == 0:
            return 0
        complete_steps = sum([pi.complete_steps for pi in pis])
        return int((complete_steps / total_steps) * 100)


class ProcessInstance(HasTimeStampsMixin):
    class Meta:
        ordering = ["pk"]
    
    process = models.ForeignKey("workflows.Process", on_delete=models.CASCADE)
    workflow_instance = models.ForeignKey(WorkflowInstance, on_delete=models.CASCADE)
    current_step_instance = models.ForeignKey("workflows.StepInstance", blank=True, null=True, on_delete=models.SET_NULL)

    @property
    def percent_complete(self):
        if not self.current_step_instance:
            return 100
        else:
            num_steps_before = self.current_step_instance.step.num_steps_before
            print("PI STEPS", self.pk, num_steps_before)
            num_steps_after = self.current_step_instance.step.num_steps_after
            total_steps = num_steps_before + 1 + num_steps_after
            return int((num_steps_before / total_steps) * 100)

    @property
    def total_steps(self):
        return self.process.total_steps
    
    @property
    def complete_steps(self):
        if not self.current_step_instance:
            return self.total_steps
        else:
            return self.current_step_instance.step.num_steps_before


class StepInstance(HasTimeStampsMixin):
    class Meta:
        ordering = ["pk"]
    
    step = models.ForeignKey(Step, on_delete=models.CASCADE)
    process_instance = models.ForeignKey(ProcessInstance, on_delete=models.CASCADE)
    completed_by = models.ForeignKey("people.Employee", blank=True, null=True, on_delete=models.SET_NULL)

    @property
    def is_complete(self):
        return bool(self.completed_by)

    #TODO: Complete method fills completed_at, completed_by, and current_step_instance and completed_at on Workflow instance
