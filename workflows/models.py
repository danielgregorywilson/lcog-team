from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _

from people.models import Employee, UnitOrProgram


class Role(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    members = models.ManyToManyField(
        "people.Employee", related_name="workflow_roles", blank=True
    )


class EmployeeTransition(models.Model):
    TRANSITION_TYPE_NEW = 'N'
    TRANSITION_TYPE_RETURN = 'R'
    TRANSITION_TYPE_CHANGE = 'C'
    TRANSITION_TYPE_EXIT = 'E'
    TRANSITION_TYPE_CHOICES = [
        (TRANSITION_TYPE_NEW, 'New'),
        (TRANSITION_TYPE_RETURN, 'Return'),
        (TRANSITION_TYPE_CHANGE, 'Change/Modify'),
        (TRANSITION_TYPE_EXIT, 'Exit')
    ]

    EMPLOYEE_ID_CLSD = 'CLSD'
    EMPLOYEE_ID_CLID = 'CLID'
    EMPLOYEE_ID_CHOICES = [
        (EMPLOYEE_ID_CLSD, 'CLSD'),
        (EMPLOYEE_ID_CLID, 'CLID')
    ]

    LOCATION_COTTAGE_GROVE = 'CG'
    LOCATION_FLORENCE = 'FL'
    LOCATION_JUNCTION_CITY = 'JC'
    LOCATION_OAKRIDGE = 'OA'
    LOCATION_PP4 = 'P4'
    LOCATION_PP5 = 'P5'
    LOCATION_SB = 'SB'
    LOCATION_S1 = 'S1'
    LOCATION_S2 = 'S2'
    LOCATION_S3 = 'S3'
    LOCATION_SENIOR_MEALS = 'SM'
    LOCATION_VENETA = 'VE'
    LOCATION_CHOICES = [
        (LOCATION_COTTAGE_GROVE, 'Cottage Grove'),
        (LOCATION_FLORENCE, 'Florence'),
        (LOCATION_JUNCTION_CITY, 'Junction City'),
        (LOCATION_OAKRIDGE, 'Oakridge'),
        (LOCATION_PP4, 'PPB - 4th Floor'),
        (LOCATION_PP5, 'PPB - 5th Floor'),
        (LOCATION_SB, 'Schaefers - Basement'),
        (LOCATION_S1, 'Schaefers - 1st Floor'),
        (LOCATION_S2, 'Schaefers - 2nd Floor'),
        (LOCATION_S3, 'Schaefers - 3rd Floor'),
        (LOCATION_SENIOR_MEALS, 'Senior Meals Site'),
        (LOCATION_VENETA, 'Veneta'),   
    ]

    UNION_NON_REPRESENTED = 'N'
    UNION_EA = 'E'
    UNION_SEIU = 'S'
    UNION_MANAGEMENT = 'M'
    UNION_CHOICES = [
        (UNION_NON_REPRESENTED, 'Non-Represented'),
        (UNION_EA, 'EA'),
        (UNION_SEIU, 'SEIU'),
        (UNION_MANAGEMENT, 'Management')
    ]

    PHONE_REQUEST_NEW = 'NN'
    PHONE_REQUEST_REMOVE = 'RP'
    PHONE_REQUEST_DELETE_NUM = 'DN'
    PHONE_REQUEST_REASSIGN = 'RT'
    PHONE_REQIUEST_CHANGE = 'CN'
    PHONE_REQUEST_DELETE_VM = 'DV'
    PHONE_REQUEST_CHOICES = [
        (PHONE_REQUEST_NEW, 'New number needed'),
        (PHONE_REQUEST_REMOVE, 'Remove phone'),
        (PHONE_REQUEST_DELETE_NUM, 'Delete number'),
        (PHONE_REQUEST_REASSIGN, 'Reassign to:'),
        (PHONE_REQIUEST_CHANGE, 'Change name display to:'),
        (PHONE_REQUEST_DELETE_VM, 'Delete voicemail box')
    ]

    class Meta:
        ordering = ["pk"]

    type = models.CharField(
        _("transition type"), max_length=1, choices=TRANSITION_TYPE_CHOICES,
        blank=True, null=True
    )
    # TODO: What does this mean now?
    date_submitted = models.DateTimeField(blank=True, null=True) 
    submitter = models.ForeignKey(
        Employee, blank=True, null=True, on_delete=models.SET_NULL,
        related_name="submitter_of_transitions"
    )
    employee_first_name = models.CharField(blank=True, max_length=50)
    employee_middle_initial = models.CharField(blank=True, max_length=1)
    employee_last_name = models.CharField(blank=True, max_length=50)
    employee_preferred_name = models.CharField(blank=True, max_length=100)
    employee_number = models.PositiveSmallIntegerField(blank=True, null=True)
    employee_id = models.CharField(blank=True, max_length=4, choices=EMPLOYEE_ID_CHOICES)
    employee_email = models.EmailField(blank=True)
    title = models.CharField(blank=True, max_length=100)
    fte = models.FloatField(blank=True, default=1.0)
    salary_range = models.PositiveSmallIntegerField(blank=True, null=True)
    salary_step = models.PositiveSmallIntegerField(blank=True, null=True)
    bilingual = models.BooleanField(default=False)
    manager = models.ForeignKey(
        Employee, blank=True, null=True, on_delete=models.SET_NULL,
        related_name="manager_of_transitions"
    )
    unit = models.ForeignKey(
        UnitOrProgram, blank=True, null=True, on_delete=models.SET_NULL
    )
    transition_date = models.DateTimeField(blank=True, null=True)
    preliminary_hire = models.BooleanField(default=False)
    delete_profile = models.BooleanField(default=False)
    office_location = models.CharField(max_length=4, choices=LOCATION_CHOICES)
    cubicle_number = models.PositiveSmallIntegerField(blank=True, null=True)
    union_affiliation = models.CharField(max_length=2, choices=UNION_CHOICES)
    teleworking = models.BooleanField(default=False)
    current_phone = models.CharField(max_length=10, blank=True)
    desk_phone = models.BooleanField(default=False)
    phone_request = models.CharField(max_length=3, choices=PHONE_REQUEST_CHOICES, blank=True)
    phone_request_data = models.CharField(max_length=50, blank=True)
    load_code = models.CharField(max_length=50, blank=True)
    should_delete = models.BooleanField(default=False)
    reassign_to = models.CharField(max_length=50, blank=True)
    business_cards = models.BooleanField(default=False)
    prox_card_needed = models.BooleanField(default=False)
    prox_card_returned = models.BooleanField(default=False)
    access_emails = models.ForeignKey(
        Employee, blank=True, null=True, on_delete=models.SET_NULL,
        related_name="access_emails_after_transitions"
    )
    special_instructions = models.TextField(blank=True)


class Workflow(models.Model):
    """
    A high-level workflow, e.g. new employee onboarding.
    """
    class Meta:
        ordering = ["pk"]
    
    def __str__(self):
        return f"Workflow: {self.name}"
    
    name = models.CharField(max_length=100)
    role = models.ForeignKey(
        Role, blank=True, null=True, on_delete=models.SET_NULL,
        help_text=_(
            "The set of employees with full admin access to this workflow"
        )
    )
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
    workflow = models.ForeignKey(
        Workflow, related_name="processes", on_delete=models.CASCADE
    )
    workflow_start = models.BooleanField(
        default=False,
        help_text=_("Start this process when a workflow begins.")
    )
    role = models.ForeignKey(
        Role, blank=True, null=True, on_delete=models.SET_NULL,
        help_text=_(
            "The set of employees with full admin access to this process"
        )
    )
    version = models.IntegerField(default=1)

    @property
    def total_steps(self):
        return self.step_set.filter(end=True).first().num_steps_before + 1

    def create_process_instance(self, wfi):
        pi = ProcessInstance.objects.create(
            process=self, workflow_instance=wfi
        )
        first_step = self.step_set.filter(start=True)[0]
        si = StepInstance.objects.create(step=first_step, process_instance=pi)
        pi.current_step_instance = si
        pi.save()

    #TODO: Complete when step marked "end" is completed
    #TODO: On save, make sure there is a start and end step if there are any steps


class Action(models.Model):
    LINK = 'LINK'
    API = 'API'
    EMAIL = 'EMAIL'
    ACTION_TYPE_CHOICES = [
        (LINK, 'Navigate to Link'),
        (API, 'Make API call'),
        (EMAIL, 'Send an email'),
    ]
    
    type = models.CharField(
        _("action type"), max_length=5, choices=ACTION_TYPE_CHOICES,
        blank=True, null=True
    )
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
    order = models.IntegerField(
        help_text=_("Display order in admin Process detail"), default=0
    )
    start = models.BooleanField(default=False)
    end = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    role = models.ForeignKey(
        Role, blank=True, null=True, on_delete=models.SET_NULL,
        help_text=_(
            "The set of employees responsible for completing this step"
        )
    )
    next_step = models.ForeignKey(
        "self", blank=True, null=True, on_delete=models.SET_NULL,
        help_text=_("The next step, when there is only one")
    )
    choices_prompt = models.CharField(
        max_length=200, blank=True,
        help_text=_("The prompt for when there are multiple next step choices")
    )
    trigger_processes = models.ManyToManyField(
        Process, related_name="triggering_steps", blank=True
    )
    completion_action = models.ForeignKey(
        Action, blank=True, null=True, on_delete=models.SET_NULL,
        help_text=_("Action to trigger as this step completes")
    )
    optional_actions = models.ManyToManyField(
        Action, blank=True, related_name="triggering_steps"
    )

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
                previous_step = Step.objects.filter(
                    next_step=current_step
                ).first()
                if not previous_step:
                    # In the case of a choice, there is no next step, so find
                    # the step that leads to this one with choices.
                    step_choice = StepChoice.objects.filter(
                        next_step=current_step
                    ).first()
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
        current_step = self
        while True:
            if current_step.end == True:
                break
            else:
                if current_step.next_step:
                    current_step = current_step.next_step
                else:
                    step_choice = StepChoice.objects.filter(
                        step=current_step
                    ).first()
                    if not step_choice:
                        raise Exception("Couldn't find a next step.")
                    current_step = step_choice.next_step
        return num_steps

    #TODO: On save, error if no next and not end
    #TODO: Properties for next step, previous step, is first step and is last step


class StepChoice(models.Model):
    step = models.ForeignKey(
        Step, related_name="next_step_choices", on_delete=models.CASCADE
    )
    order = models.IntegerField(
        help_text=_("Display order in admin Step detail"), default=0
    )
    choice_text = models.CharField(max_length=100)
    next_step = models.ForeignKey(
        Step, blank=True, null=True, on_delete=models.SET_NULL
    )


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
    transition = models.OneToOneField(
        EmployeeTransition, blank=True, null=True, on_delete=models.SET_NULL
    )

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
    
    @property
    def employee_name(self):
        if self.transition:
            return f'{self.transition.employee_first_name} {self.transition.employee_last_name}'
    
    @property
    def title(self):
        if self.transition:
            return self.transition.title
    
    @property
    def transition_date(self):
        if self.transition:
            return self.transition.transition_date


class ProcessInstance(HasTimeStampsMixin):
    class Meta:
        ordering = ["pk"]
    
    process = models.ForeignKey("workflows.Process", on_delete=models.CASCADE)
    workflow_instance = models.ForeignKey(
        WorkflowInstance, on_delete=models.CASCADE
    )
    current_step_instance = models.ForeignKey(
        "workflows.StepInstance", blank=True, null=True,
        on_delete=models.SET_NULL
    )

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
    process_instance = models.ForeignKey(
        ProcessInstance, on_delete=models.CASCADE
    )
    completed_by = models.ForeignKey(
        "people.Employee", blank=True, null=True, on_delete=models.SET_NULL
    )

    @property
    def is_complete(self):
        return bool(self.completed_by)

    #TODO: Complete method fills completed_at, completed_by, and current_step_instance and completed_at on Workflow instance
