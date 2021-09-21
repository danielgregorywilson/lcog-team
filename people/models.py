import datetime
from mainsite.models import SecurityMessage

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from mainsite.helpers import (
    send_completed_email_to_hr_manager,
    send_signature_email_to_executive_director,
    send_signature_email_to_hr_manager
)
from mainsite.models import SecurityMessage


# SHOW_REVIEW_TO_MANAGER_DAYS_BEFORE_DUE = 60
SHOW_REVIEW_TO_MANAGER_DAYS_BEFORE_DUE = 360


class Division(models.Model):
    class Meta:
        verbose_name = _("Division")
        verbose_name_plural = _("Divisions")
        ordering = ["name"]

    name = models.CharField(_("name"), max_length=100)

    def __str__(self):
        return self.name


class UnitOrProgram(models.Model):
    class Meta:
        verbose_name = _("Unit/Program")
        verbose_name_plural = _("Units/Programs")
        ordering = ["division__name", "name"]

    division = models.ForeignKey("people.Division", verbose_name=_("division"), on_delete=models.CASCADE)
    name = models.CharField(_("name"), max_length=100)

    def __str__(self):
        return f"{self.division.name} : {self.name}"


class JobTitle(models.Model):
    class Meta:
        verbose_name = _("Job Title")
        verbose_name_plural = _("Job Titles")

    name = models.CharField(_("name"), max_length=100)
    position_description_link = models.URLField(_("position description link"), blank=True, null=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")
        ordering = ["user__username"]

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("employee_detail", kwargs={"pk": self.pk})

    def username(self):
        return self.user.username

    user = models.OneToOneField("auth.User", verbose_name=_("user"), on_delete=models.CASCADE)
    manager = models.ForeignKey("self", related_name="direct_reports", blank=True, null=True, verbose_name=_("manager"), on_delete=models.SET_NULL)
    unit_or_program = models.ForeignKey("people.UnitOrProgram", verbose_name=_("unit/program"), on_delete=models.SET_NULL, blank=True, null=True)
    job_title = models.ForeignKey("people.JobTitle", verbose_name=_("job title"), on_delete=models.SET_NULL, blank=True, null=True)
    position_description_link_override = models.URLField(_("position description link override"), blank=True, null=True)

    is_division_director = models.BooleanField(_("is a division director"), default=False)
    
    # These are UNIQUELY TRUE, enforced in model save
    is_hr_manager = models.BooleanField(_("is the HR manager"), default=False)
    is_executive_director = models.BooleanField(_("is the executive director"), default=False)

    viewed_security_message = models.BooleanField(_("has viewed security message"), default=False)

    @property
    def is_program_manager(self):
        return not self.is_executive_director and self.manager.is_division_director

    @property
    def has_program_manager(self):
        current_employee = self
        if current_employee.is_executive_director:
            return False
        if current_employee.is_division_director:
            return False
        if current_employee.manager.is_division_director:
            return False
        while True:
            if current_employee.manager.is_division_director:
                return True
            if current_employee.manager:
                current_employee = current_employee.manager
            else:
                return False

    @property
    def get_program_manager(self):
        current_employee = self
        if current_employee.manager.is_division_director:
            return None
        while True:
            if current_employee.manager.is_division_director:
                return current_employee
            if current_employee.manager:
                current_employee = current_employee.manager
            else:
                return None

    @property
    def has_division_director(self):
        current_employee = self
        if current_employee.is_division_director:
            return False
        while True:
            if current_employee.is_division_director:
                return True
            if current_employee.manager:
                current_employee = current_employee.manager
            else:
                return False

    @property
    def get_division_director(self):
        current_employee = self
        if current_employee.is_division_director:
            return None
        while True:
            if current_employee.is_division_director:
                return current_employee
            if current_employee.manager:
                current_employee = current_employee.manager
            else:
                return None

    def save(self, *args, **kwargs):
        # is_hr_manager can only apply to ONE Employee
        if self.is_hr_manager:
            try:
                old_manager = Employee.objects.get(is_hr_manager=True)
                if self != old_manager:
                    old_manager.is_hr_manager = False
                    old_manager.save()
            except Employee.DoesNotExist:
                pass
        # is_executive_director can only apply to ONE Employee
        if self.is_executive_director:
            try:
                old_director = Employee.objects.get(is_executive_director=True)
                if self != old_director:
                    old_director.is_executive_director = False
                    old_director.save()
            except Employee.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def employee_next_review(self):
        return self.performancereview_set.all().order_by("period_end_date").first()

    def get_direct_reports(self):
        return self.direct_reports.all()
    
    def get_descendants_of_employee(self, employee):
        employee_and_descendants = [employee]
        descendants = employee.direct_reports.all()
        for descendant in descendants:
            employee_and_descendants += self.get_descendants_of_employee(descendant)
        return employee_and_descendants

    def get_direct_reports_descendants(self, include_self=False):
        # Return all descendant direct reports, including the user's direct
        # reports.
        direct_reports_descendants = [self.get_descendants_of_employee(employee) for employee in self.get_direct_reports()]
        flat_list = [item for sublist in direct_reports_descendants for item in sublist] # Flatten the 2-D list
        pk_list = [item.pk for item in flat_list]
        if include_self:
            pk_list.append(self.pk)
        unique_descendant_pks = list(set(pk_list))
        return Employee.objects.filter(pk__in=unique_descendant_pks)

    def manager_upcoming_reviews(self):
        reviews = []
        for employee in self.get_direct_reports():
            employee_reviews = employee.performancereview_set.all()
            for review in employee_reviews:
                if review.days_until_due() < SHOW_REVIEW_TO_MANAGER_DAYS_BEFORE_DUE:
                    reviews.append(review)
        return sorted(reviews, key=lambda review: review.period_end_date)
    
    def manager_upcoming_reviews_action_required(self):
        reviews = []
        for review in self.manager_upcoming_reviews():
            if review.status == PerformanceReview.NEEDS_EVALUATION:
                reviews.append(review)
        return reviews
    
    def manager_upcoming_reviews_no_action_required(self):
        reviews = []
        for review in self.manager_upcoming_reviews():
            if review.status != PerformanceReview.NEEDS_EVALUATION:
                reviews.append(review)
        return reviews

    def signature_all_relevant_upcoming_reviews(self):
        # Returns all upcoming reviews for a manager's direct reports and their
        # descendants. For detail views.
        reviews = []
        for employee in self.get_direct_reports():
            employee_reviews = employee.performancereview_set.all()
            for review in employee_reviews:
                if review.days_until_due() < SHOW_REVIEW_TO_MANAGER_DAYS_BEFORE_DUE:
                    reviews.append(review)
        for employee in self.get_direct_reports_descendants():
            employee_reviews = employee.performancereview_set.all()
            for review in employee_reviews:
                if review.days_until_due() < SHOW_REVIEW_TO_MANAGER_DAYS_BEFORE_DUE:
                    reviews.append(review)
        return sorted(reviews, key=lambda review: review.period_end_date)
    
    def signature_upcoming_reviews(self):
        # Returns all upcoming reviews for a manager's direct reports.
        # HR Manager and Executive Director should see upcoming reviews for all
        # Employees.
        reviews = []
        if self.is_hr_manager:
            employees = Employee.objects.all()
        elif self.is_hr_manager:
            employees = Employee.objects.all()
        else:
            employees = self.get_direct_reports_descendants()
        for employee in employees:
            employee_reviews = employee.performancereview_set.all()
            for review in employee_reviews:
                if review.days_until_due() < SHOW_REVIEW_TO_MANAGER_DAYS_BEFORE_DUE:
                    reviews.append(review)
        return sorted(reviews, key=lambda review: review.period_end_date)
    
    def signature_upcoming_reviews_action_required(self):
        # Returns all upcoming reviews for a manager's direct reports which
        # require action from the manager to proceed. For list views.
        reviews = []
        for review in self.signature_upcoming_reviews():
            if self.is_executive_director:
                if (
                    review.status == PerformanceReview.EVALUATION_HR_PROCESSED and
                    review.signature_set.filter(employee=self).count() == 0
                ):
                    reviews.append(review)
            elif self.is_hr_manager:
                if (
                    review.status == PerformanceReview.EVALUATION_APPROVED and
                    review.signature_set.filter(employee=self).count() == 0
                ):
                    reviews.append(review)
            else:
                direct_report = review.employee
                while direct_report.manager != self:
                    direct_report = direct_report.manager
                if (
                    review.status == PerformanceReview.EVALUATION_WRITTEN and
                    review.signature_set.filter(employee=direct_report).count() == 1 and
                    review.signature_set.filter(employee=self).count() == 0
                ):
                    reviews.append(review)
        return reviews
    
    def signature_upcoming_reviews_no_action_required(self):
        # Returns all upcoming reviews for a manager's direct reports which do
        # not require action from the manager to proceed. For list views.
        reviews = []
        for review in self.signature_upcoming_reviews():
            if review.signature_set.filter(employee=self.pk).count() > 0:
                reviews.append(review)
        return reviews

    def telework_applications_signature_required(self):
        # Returns all telework applications requiring a user's signature.
        applications = []
        # Division Director
        if self.is_division_director:
            for employee in self.get_direct_reports_descendants():
                if hasattr(employee, 'teleworkapplication') and employee.teleworkapplication.division_director_ready_to_sign():
                    applications.append(employee.teleworkapplication)
        # Program Manager
        elif self.is_program_manager:
            for employee in self.get_direct_reports_descendants():
                if hasattr(employee, 'teleworkapplication') and employee.teleworkapplication.program_manager_ready_to_sign():
                    applications.append(employee.teleworkapplication)    
        # Manager
        else:
            for employee in self.direct_reports.all():
                if hasattr(employee, 'teleworkapplication') and employee.teleworkapplication.manager_ready_to_sign():
                    applications.append(employee.teleworkapplication)
        return sorted(applications, key=lambda application: application.date)
    
    def telework_applications_signature_not_required(self):
        # Returns all telework applications signed by the user
        applications = []
        # Division Director
        if self.is_division_director:
            for employee in self.get_direct_reports_descendants():
                if hasattr(employee, 'teleworkapplication') and employee.teleworkapplication.division_director_signed():
                    applications.append(employee.teleworkapplication)
        # Program Manager
        elif self.is_program_manager:
            for employee in self.get_direct_reports_descendants():
                if hasattr(employee, 'teleworkapplication') and employee.teleworkapplication.program_manager_signed():
                    applications.append(employee.teleworkapplication)
        # Manager
        else:
            for employee in self.direct_reports.all():
                if hasattr(employee, 'teleworkapplication') and employee.teleworkapplication.manager_signed():
                    applications.append(employee.teleworkapplication)
        return sorted(applications, key=lambda application: application.date)

    def prs_can_view(self):
        # You can view all PRs for which either you are the employee or the
        # employee is your direct report or a descendant direct report.
        if self.is_hr_manager or self.is_executive_director:
            return map(lambda pr: pr.id, PerformanceReview.objects.all())
        self_and_direct_reports = self.get_direct_reports_descendants(include_self=True)
        pr_ids = []
        for employee in self_and_direct_reports:
            employee_pr_ids = map(lambda pr: pr.id, PerformanceReview.objects.filter(employee=employee))
            pr_ids += employee_pr_ids
        return list(pr_ids)
    
    def notes_can_view(self):
        # You can view all notes you wrote.
        note_ids = map(lambda note: note.id, ReviewNote.objects.filter(manager=self))
        return list(note_ids)

    def telework_applications_can_view(self):
        # You can view all Telework Applications for which either you are the employee or the
        # employee is your direct report or a descendant direct report.
        if self.is_hr_manager or self.is_executive_director:
            return map(lambda pr: pr.id, TeleworkApplication.objects.all())
        self_and_direct_reports = self.get_direct_reports_descendants(include_self=True)
        application_ids = []
        for employee in self_and_direct_reports:
            employee_application_ids = map(lambda pr: pr.id, TeleworkApplication.objects.filter(employee=employee))
            application_ids += employee_application_ids
        return list(application_ids)

    def position_description_link(self):
        # Returns override link if provided, otherwise the link from job title if there is a job title
        if self.position_description_link_override:
            return self.position_description_link_override
        elif self.job_title and self.job_title.position_description_link:
            return self.job_title.position_description_link
        return None


class ManagerUpcomingReviewsManager(models.Manager):
    def get_queryset(self, user):
        queryset = super().get_queryset()
        if hasattr(user, 'employee'):
            desired_pks = [pr.pk for pr in user.employee.manager_upcoming_reviews()]
            queryset = queryset.filter(pk__in=desired_pks)
        return queryset


class ManagerUpcomingReviewsActionRequiredManager(models.Manager):
    def get_queryset(self, user):
        queryset = super().get_queryset()
        desired_pks = [pr.pk for pr in user.employee.manager_upcoming_reviews_action_required()]
        queryset = queryset.filter(pk__in=desired_pks)
        return queryset


class ManagerUpcomingReviewsNoActionRequiredManager(models.Manager):
    def get_queryset(self, user):
        queryset = super().get_queryset()
        desired_pks = [pr.pk for pr in user.employee.manager_upcoming_reviews_no_action_required()]
        queryset = queryset.filter(pk__in=desired_pks)
        return queryset


class SignatureAllRelevantUpcomingReviewsManager(models.Manager):
    def get_queryset(self, user):
        queryset = super().get_queryset()
        desired_pks = [pr.pk for pr in user.employee.signature_all_relevant_upcoming_reviews()]
        queryset = queryset.filter(pk__in=desired_pks)
        return queryset


class SignatureUpcomingReviewsActionRequiredManager(models.Manager):
    def get_queryset(self, user):
        queryset = super().get_queryset()
        desired_pks = [pr.pk for pr in user.employee.signature_upcoming_reviews_action_required()]
        queryset = queryset.filter(pk__in=desired_pks)
        return queryset


class SignatureUpcomingReviewsNoActionRequiredManager(models.Manager):
    def get_queryset(self, user):
        queryset = super().get_queryset()
        desired_pks = [pr.pk for pr in user.employee.signature_upcoming_reviews_no_action_required()]
        queryset = queryset.filter(pk__in=desired_pks)
        return queryset


class PerformanceReview(models.Model):
    class Meta:
        verbose_name = _("Performance Review")
        verbose_name_plural = _("Performance Reviews")
        ordering = ["-pk"]

    def __str__(self):
        return f"Performance review for {self.employee.user.username} on {self.period_end_date}"

    def get_absolute_url(self):
        return reverse("performance_review_detail", kwargs={"pk": self.pk})

    # Managers for filtering PRs
    objects = models.Manager()
    manager_upcoming_reviews = ManagerUpcomingReviewsManager()
    manager_upcoming_reviews_action_required = ManagerUpcomingReviewsActionRequiredManager()
    manager_upcoming_reviews_no_action_required = ManagerUpcomingReviewsNoActionRequiredManager()
    signature_all_relevant_upcoming_reviews = SignatureAllRelevantUpcomingReviewsManager()
    signature_upcoming_reviews_action_required = SignatureUpcomingReviewsActionRequiredManager()
    signature_upcoming_reviews_no_action_required = SignatureUpcomingReviewsNoActionRequiredManager()

    NEEDS_EVALUATION = 'N'
    EVALUATION_WRITTEN = 'EW'
    EVALUATION_APPROVED = 'EA'
    EVALUATION_HR_PROCESSED = 'EP'
    EVALUATION_ED_APPROVED = 'ED'
    STATUS_CHOICE = [
        (NEEDS_EVALUATION, 'Needs evaluation'),
        (EVALUATION_WRITTEN, 'Evaluation written and reviewed with employee'),
        (EVALUATION_APPROVED, 'Evaluation approved up to division director'),
        (EVALUATION_HR_PROCESSED, 'Evaluation processed by HR'),
        (EVALUATION_ED_APPROVED, 'Evaluation approved by executive director'),
    ]

    PROBATIONARY_EVALUATION = 'P'
    ANNUAL_EVALUATION = 'A'
    EVALUATION_TYPE_CHOICE = [
        (PROBATIONARY_EVALUATION, 'Probationary evaluation'),
        (ANNUAL_EVALUATION, 'Annual evaluation'),
    ]

    SEIU_PROBATIONARY_EVALUATION = 'S'
    NON_SEIU_PROBATIONARY_EVALUATION = 'N'
    PROBATIONARY_EVALUATION_TYPE_CHOICE = [
        (NON_SEIU_PROBATIONARY_EVALUATION, 'SEIU (180 day)'),
        (NON_SEIU_PROBATIONARY_EVALUATION, 'Non-SEIU (6 month)'),
    ]

    YES = 'Y'
    NO = 'N'
    NULLABLE_BOOLEAN_CHOICE = [
        (YES, 'Yes'),
        (NO, 'No')
    ]

    NEEDS_IMPROVEMENT = 'N'
    MEETS_JOB_REQUIREMENTS = 'M'
    EXCEEDS_JOB_REQUIREMENTS = 'E'
    NOT_APPLICABLE = 'NA'
    PERFORMANCE_FACTOR_CHOICE = [
        (NEEDS_IMPROVEMENT, 'Needs Improvement'),
        (MEETS_JOB_REQUIREMENTS, 'Meets Job Requirements'),
        (EXCEEDS_JOB_REQUIREMENTS, 'Exceeds Job Requirements'),
        (NOT_APPLICABLE, 'Not Applicable'),
    ]

    status = models.CharField(_("review status"), max_length=2, choices=STATUS_CHOICE, default=NEEDS_EVALUATION)

    employee = models.ForeignKey("Employee", verbose_name=_("employee"), on_delete=models.CASCADE)
    period_start_date = models.DateField(_("performance period start date"), auto_now=False, auto_now_add=False)
    period_end_date = models.DateField(_("performance period end date"), auto_now=False, auto_now_add=False)
    effective_date = models.DateField(_("effective date"), auto_now=False, auto_now_add=False)

    evaluation_type = models.CharField(_("evaluation type"), max_length=1, choices=EVALUATION_TYPE_CHOICE, default=ANNUAL_EVALUATION, blank=True, null=True)
    probationary_evaluation_type = models.CharField(_("probationary evaluation type"), max_length=1, choices=PROBATIONARY_EVALUATION_TYPE_CHOICE, blank=True, null=True)

    step_increase = models.CharField(_("step increase"), max_length=1, choices=NULLABLE_BOOLEAN_CHOICE, blank=True, null=True)
    top_step_bonus = models.CharField(_("top step bonus"), max_length=1, choices=NULLABLE_BOOLEAN_CHOICE, blank=True, null=True)
    action_other = models.CharField(_("action other"), max_length=255, blank=True, null=True)
    
    factor_job_knowledge = models.CharField(_("job knowledge"), max_length=2, choices=PERFORMANCE_FACTOR_CHOICE, blank=True, null=True)
    factor_work_quality = models.CharField(_("quality of work"), max_length=2, choices=PERFORMANCE_FACTOR_CHOICE, blank=True, null=True)
    factor_work_quantity = models.CharField(_("quanitity of work"), max_length=2, choices=PERFORMANCE_FACTOR_CHOICE, blank=True, null=True)
    factor_work_habits = models.CharField(_("work habits"), max_length=2, choices=PERFORMANCE_FACTOR_CHOICE, blank=True, null=True)
    factor_analysis = models.CharField(_("analysis and decision-making"), max_length=2, choices=PERFORMANCE_FACTOR_CHOICE, blank=True, null=True)
    factor_initiative = models.CharField(_("initiative and creativity"), max_length=2, choices=PERFORMANCE_FACTOR_CHOICE, blank=True, null=True)
    factor_interpersonal = models.CharField(_("interpersonal relations"), max_length=2, choices=PERFORMANCE_FACTOR_CHOICE, blank=True, null=True)
    factor_communication = models.CharField(_("communication"), max_length=2, choices=PERFORMANCE_FACTOR_CHOICE, blank=True, null=True)
    factor_dependability = models.CharField(_("dependability and responsibility"), max_length=2, choices=PERFORMANCE_FACTOR_CHOICE, blank=True, null=True)
    factor_professionalism = models.CharField(_("professionalism and customer service"), max_length=2, choices=PERFORMANCE_FACTOR_CHOICE, blank=True, null=True)
    factor_management = models.CharField(_("project management"), max_length=2, choices=PERFORMANCE_FACTOR_CHOICE, blank=True, null=True)
    factor_supervision = models.CharField(_("supervision"), max_length=2, choices=PERFORMANCE_FACTOR_CHOICE, blank=True, null=True)

    evaluation_successes = models.TextField(_("employee's successes"), blank=True, null=True)
    evaluation_opportunities = models.TextField(_("opportunities for growth"), blank=True, null=True)
    evaluation_goals_manager = models.TextField(_("goals for the comind year (manager)"), blank=True, null=True)
    evaluation_goals_employee = models.TextField(_("goals for the comind year (employee)"), blank=True, null=True)
    evaluation_comments_employee = models.TextField(_("employee comments"), blank=True, null=True)

    description_reviewed_employee = models.BooleanField(_("position description has been reviewed with employee"), default=False)
    signed_position_description = models.FileField(_("signed position description"), upload_to="uploads/signed-position-descriptions", blank=True, null=True)

    def username(self):
        return self.employee.user.username

    def days_until_due(self):
        timedelta = self.effective_date - datetime.date.today()
        return timedelta.days

    def overdue(self):
        if self.days_until_due() <= 0:
            return True
        return False

    def employee_has_signed(self, employee):
        return Signature.objects.filter(review=self, employee=employee).count()

    def all_required_signatures(self):
        """
        Returns a list of lists of the form:
        (
            Employee Title, Employee Name, Signature Date, Employee PK,
            Whether the Employee is ready to sign and needs to sign
        )
        such that each tuple represents a signature required or already created
        for the Performance Review to be completed. Starts with the Employee
        and proceeds up the management chain until it gets to the Division
        Director. And then we add HR Manager and Executive Director.
        """
        signatures = []
        employee = self.employee
        employee_signature = Signature.objects.filter(review=self, employee=self.employee).first()
        last_employee_in_chain = employee # Keep track of the last employee so we can check if they signed
        added_hr_manager = False
        added_executive_director = False
        while True:
            # Try to get the current Employee's signature and add it to the signature list
            if len(signatures) == 0:
                title = "Employee"
            elif len(signatures) == 1:
                title = "Manager"
            else:
                if employee.job_title:
                    title = employee.job_title.name
                else:
                    title = None
            signature = Signature.objects.filter(review=self, employee=employee).first()
            if signature:
                signatures.append([title, signature.employee.user.get_full_name(), signature.date, None, False]) # Not ready to sign because there is a signature
            else:
                ready_to_sign = False
                if title in ["Employee", "Manager"]:
                    if self.status != PerformanceReview.NEEDS_EVALUATION:
                        ready_to_sign = True
                else:
                    # If direct report has signed, we are ready
                    direct_report_signature = Signature.objects.filter(review=self, employee=last_employee_in_chain).first()
                    if direct_report_signature and employee_signature:
                        ready_to_sign = True
                signatures.append([title, None, None, employee.pk, ready_to_sign])
            
            # Keep track of whether we're already adding HR manager and ED signatures
            if employee.is_hr_manager:
                added_hr_manager = True
            if employee.is_executive_director:
                added_executive_director = True

            # Get the next manager in the chain
            if employee.is_division_director:
                break
            if employee.manager:
                last_employee_in_chain = employee
                employee = employee.manager
            else:
                break
        
        # Finally, add the HR Manager and Executive Director Signatures if still needed
        if not added_hr_manager:
            hr_manager = Employee.objects.filter(is_hr_manager=True).first()
            hr_signature = Signature.objects.filter(review=self, employee=hr_manager).first()
            if hr_signature:
                signatures.append(["Human Resources Manager", hr_manager.user.get_full_name(), hr_signature.date, None, False]) # Not ready to sign because there is a signature
            else:
                # If last manager has signed, we are ready
                direct_report_signature = Signature.objects.filter(review=self, employee=last_employee_in_chain).first()
                ready_to_sign = False
                if direct_report_signature:
                    ready_to_sign = True
                signatures.append(["Human Resources Manager", None, None, hr_manager.pk, ready_to_sign])
        if not added_executive_director:
            ed = Employee.objects.filter(is_executive_director=True).first()
            ed_signature = Signature.objects.filter(review=self, employee=ed).first()
            if ed_signature:
                signatures.append(["Executive Director", ed.user.get_full_name(), ed_signature.date, None, False]) # Not ready to sign because there is a signature
            else:
                # If HR manager has signed, we are ready
                ready_to_sign = False
                if hr_signature:
                    ready_to_sign = True
                signatures.append(["Executive Director", None, None, ed.pk, ready_to_sign])
        return signatures

    def create_next_review_for_employee(self):
        PerformanceReview.objects.create(
            employee=self.employee,
            period_start_date=self.period_end_date,
            period_end_date=self.period_end_date + datetime.timedelta(days=365),
            effective_date=self.effective_date + datetime.timedelta(days=365),
            evaluation_type=self.ANNUAL_EVALUATION
        )


class SignatureReminder(models.Model):
    """
    Represents the last time an employee was reminded to sign a Performance
    Evaluation. We can use this to remind them again a specific amount of time
    in the future.
    """
    
    class Meta:
        verbose_name = _("Signature Reminder")
        verbose_name_plural = _("Signature Reminders")
        get_latest_by = ("date")

    def __str__(self):
        if self.employee == self.review.employee:
            return f"Reminder for {self.employee.user.username} on {self.date} to sign their own review"
        elif self.employee == self.review.employee.manager:
            return f"Reminder for {self.employee.user.username} on {self.date} to sign a review for {self.review.employee.user.username} that they wrote"
        else:
            return f"Reminder for {self.employee.user.username} on {self.date} to sign a review for {self.review.employee.user.username}"

    review = models.ForeignKey("people.PerformanceReview", verbose_name=_("performance review"), on_delete=models.CASCADE)
    employee = models.ForeignKey("people.Employee", on_delete=models.CASCADE)
    date = models.DateField(_("reminder date"), auto_now=False, auto_now_add=True)
    next_date = models.DateField(_("planned next reminder date"))


class Signature(models.Model):    
    class Meta:
        verbose_name = _("PR Signature")
        verbose_name_plural = _("PR Signatures")

    def __str__(self):
        return f"{self.employee.user.get_full_name()}'s approval of {self.review.employee.user.get_full_name()}'s performance review"

    review = models.ForeignKey("people.PerformanceReview", verbose_name=_("performance review"), on_delete=models.CASCADE)
    employee = models.ForeignKey("people.Employee", on_delete=models.CASCADE)
    date = models.DateField(_("signature date"), auto_now=False, auto_now_add=True)


class ReviewNote(models.Model):
    class Meta:
        verbose_name = _("Review Note")
        verbose_name_plural = _("Review Notes")
        ordering = ["-pk"]

    def get_absolute_url(self):
        return reverse("note-update", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if not hasattr(self, 'manager'):
            self.manager = self.employee.manager
        super().save(*args, **kwargs)

    manager = models.ForeignKey("Employee", related_name="notes_written", verbose_name=_("manager"), on_delete=models.CASCADE)
    employee = models.ForeignKey("Employee", related_name="notes", verbose_name=_("employee"), on_delete=models.CASCADE)
    date = models.DateField(_("review note date"), auto_now=False, auto_now_add=True)
    note = models.TextField(_("review note"))


class ViewedSecurityMessage(models.Model):
    employee = models.ForeignKey("people.Employee", verbose_name=_("employee"), on_delete=models.CASCADE)
    security_message = models.ForeignKey(SecurityMessage, on_delete=models.CASCADE)
    datetime = models.DateTimeField(_("viewed date"), auto_now=False, auto_now_add=True)


class AllRelevantTeleworkApplicationsManager(models.Manager):
    def get_queryset(self, user):
        if not hasattr(user, 'employee'):
            import pdb; pdb.set_trace();
        queryset = super().get_queryset()
        desired_pks = [pr.pk for pr in user.employee.all_relevant_telework_applications()]
        queryset = queryset.filter(pk__in=desired_pks)
        return queryset


class TeleworkApplicationsSignatureRequiredManager(models.Manager):
    def get_queryset(self, user):
        queryset = super().get_queryset()
        desired_pks = [pr.pk for pr in user.employee.telework_applications_signature_required()]
        queryset = queryset.filter(pk__in=desired_pks)
        return queryset


class TeleworkApplicationsSignatureNotRequiredManager(models.Manager):
    def get_queryset(self, user):
        queryset = super().get_queryset()
        desired_pks = [pr.pk for pr in user.employee.telework_applications_signature_not_required()]
        queryset = queryset.filter(pk__in=desired_pks)
        return queryset


class TeleworkApplication(models.Model):
    class Meta:
        verbose_name = _("Telework Application")
        verbose_name_plural = _("Telework Applications")
        ordering = ["-pk"]

    def __str__(self):
        return f"Telework application for {self.employee.user.username}"

    def get_absolute_url(self):
        return reverse("telework_application", kwargs={"pk": self.pk})

    # Managers for filtering PRs
    objects = models.Manager()
    all_relevant_applications = AllRelevantTeleworkApplicationsManager()
    applications_signature_required = TeleworkApplicationsSignatureRequiredManager()
    applications_signature_not_required = TeleworkApplicationsSignatureNotRequiredManager()

    INCOMPLETE = 'I'
    READY_FOR_SIGNATURE = 'R'
    APPROVED = 'A'
    STATUS_CHOICE = [
        (INCOMPLETE, 'Incomplete'),
        (READY_FOR_SIGNATURE, 'Ready for signature'),
        (APPROVED, 'Approved')
    ]

    YES = 'Y'
    NO = 'N'
    NULLABLE_BOOLEAN_CHOICE = [
        (YES, 'Yes'),
        (NO, 'No')
    ]

    employee = models.OneToOneField("Employee", verbose_name=_("employee"), on_delete=models.CASCADE)
    status = models.CharField(_("application status"), max_length=1, choices=STATUS_CHOICE, default=INCOMPLETE)

    date = models.DateField(_("date"), auto_now=False, auto_now_add=False, blank=True, null=True)
    program_manager_approve = models.CharField(_("program manager approve"), max_length=1, choices=NULLABLE_BOOLEAN_CHOICE, blank=True, null=True)

    hours_onsite = models.TextField(_("hours onsite"), blank=True, null=True)
    telework_location = models.TextField(_("telework location"), blank=True, null=True)
    hours_working = models.TextField(_("hours working"), blank=True, null=True)
    duties = models.TextField(_("duties"), blank=True, null=True)
    communication_when = models.TextField(_("communication when"), blank=True, null=True)
    communication_time = models.TextField(_("communication time"), blank=True, null=True)
    communication_how = models.TextField(_("communication how"), blank=True, null=True)

    equipment_provided_phone = models.BooleanField(_("equipment provided phone"), default=False)
    equipment_provided_laptop = models.BooleanField(_("equipment provided laptop"), default=False)
    equipment_provided_desktop = models.BooleanField(_("equipment provided desktop"), default=False)
    equipment_provided_monitor = models.BooleanField(_("equipment provided monitor"), default=False)
    equipment_provided_access = models.BooleanField(_("equipment provided access"), default=False)
    equipment_provided_other = models.BooleanField(_("equipment provided other"), default=False)
    equipment_provided_other_value = models.TextField(_("equipment provided other value"), blank=True, null=True)

    workspace_checklist_1 = models.CharField(_("workspace checklist 1"), max_length=1, choices=NULLABLE_BOOLEAN_CHOICE, blank=True, null=True)
    workspace_checklist_2 = models.CharField(_("workspace checklist 2"), max_length=1, choices=NULLABLE_BOOLEAN_CHOICE, blank=True, null=True)
    workspace_checklist_3 = models.CharField(_("workspace checklist 3"), max_length=1, choices=NULLABLE_BOOLEAN_CHOICE, blank=True, null=True)
    workspace_checklist_4 = models.CharField(_("workspace checklist 4"), max_length=1, choices=NULLABLE_BOOLEAN_CHOICE, blank=True, null=True)
    workspace_checklist_5 = models.CharField(_("workspace checklist 5"), max_length=1, choices=NULLABLE_BOOLEAN_CHOICE, blank=True, null=True)
    workspace_checklist_6 = models.CharField(_("workspace checklist 6"), max_length=1, choices=NULLABLE_BOOLEAN_CHOICE, blank=True, null=True)
    workspace_checklist_7 = models.CharField(_("workspace checklist 7"), max_length=1, choices=NULLABLE_BOOLEAN_CHOICE, blank=True, null=True)
    workspace_checklist_8 = models.CharField(_("workspace checklist 8"), max_length=1, choices=NULLABLE_BOOLEAN_CHOICE, blank=True, null=True)
    workspace_checklist_9 = models.CharField(_("workspace checklist 9"), max_length=1, choices=NULLABLE_BOOLEAN_CHOICE, blank=True, null=True)
    workspace_checklist_10 = models.CharField(_("workspace checklist 10"), max_length=1, choices=NULLABLE_BOOLEAN_CHOICE, blank=True, null=True)
    workspace_checklist_11 = models.CharField(_("workspace checklist 11"), max_length=1, choices=NULLABLE_BOOLEAN_CHOICE, blank=True, null=True)
    workspace_checklist_12 = models.CharField(_("workspace checklist 12"), max_length=1, choices=NULLABLE_BOOLEAN_CHOICE, blank=True, null=True)

    emergency_checklist_1 = models.CharField(_("emergency checklist 1"), max_length=1, choices=NULLABLE_BOOLEAN_CHOICE, blank=True, null=True)
    emergency_checklist_2 = models.CharField(_("emergency checklist 2"), max_length=1, choices=NULLABLE_BOOLEAN_CHOICE, blank=True, null=True)
    emergency_checklist_3 = models.CharField(_("emergency checklist 3"), max_length=1, choices=NULLABLE_BOOLEAN_CHOICE, blank=True, null=True)

    ergonomics_checklist_1 = models.CharField(_("emergency checklist 1"), max_length=1, choices=NULLABLE_BOOLEAN_CHOICE, blank=True, null=True)
    ergonomics_checklist_2 = models.CharField(_("emergency checklist 2"), max_length=1, choices=NULLABLE_BOOLEAN_CHOICE, blank=True, null=True)
    ergonomics_checklist_3 = models.CharField(_("emergency checklist 3"), max_length=1, choices=NULLABLE_BOOLEAN_CHOICE, blank=True, null=True)
    ergonomics_checklist_4 = models.CharField(_("emergency checklist 4"), max_length=1, choices=NULLABLE_BOOLEAN_CHOICE, blank=True, null=True)
    ergonomics_checklist_5 = models.CharField(_("emergency checklist 5"), max_length=1, choices=NULLABLE_BOOLEAN_CHOICE, blank=True, null=True)

    teleworker_comments = models.TextField(_("teleworker comments"), blank=True, null=True)
    manager_comments = models.TextField(_("manager comments"), blank=True, null=True)

    dependent_care_checklist_1 = models.CharField(_("dependent care checklist 1"), max_length=1, choices=NULLABLE_BOOLEAN_CHOICE, blank=True, null=True)
    dependent_care_documentation = models.FileField(_("dependent care documentation"), upload_to="uploads/dependent-care-documentation", blank=True, null=True)

    def username(self):
        return self.employee.user.username

    def employee_signature(self, index):
        """
        (
            Signature index, Employee Role, Employee Name, Signature Date,
            Employee PK, Whether the Employee is ready to sign
        )
        """
        signature = TeleworkSignature.objects.filter(application=self, employee=self.employee, index=index).first()
        if signature:
            return[index, "Employee", signature.employee.user.get_full_name(), signature.date, None, False] # Not ready to sign because there is a signature
        else:
            return [index, "Employee", None, None, self.employee.pk, True]

    def employee_signature_0(self):
        return self.employee_signature(0)

    def employee_signature_1(self):
        return self.employee_signature(1)

    def manager_ready_to_sign(self):
        if self.employee.manager:
            signature = TeleworkSignature.objects.filter(application=self, employee=self.employee.manager, index=0).first()
            return self.status == TeleworkApplication.READY_FOR_SIGNATURE and not signature
    
    def program_manager_ready_to_sign(self):
        if self.employee.has_program_manager:
            signature = TeleworkSignature.objects.filter(application=self, employee=self.employee.get_program_manager, index=0).first()
            return self.status == TeleworkApplication.READY_FOR_SIGNATURE and not signature
        else:
            return False

    def division_director_ready_to_sign(self):
        if self.employee.has_division_director:
            signature = TeleworkSignature.objects.filter(application=self, employee=self.employee.get_division_director, index=0).first()
            return self.status == TeleworkApplication.READY_FOR_SIGNATURE and not signature
        else:
            return False

    def manager_signed(self):
        if self.employee.manager:
            return TeleworkSignature.objects.filter(application=self, employee=self.employee.manager, index=0).count()

    def program_manager_signed(self):
        if self.employee.has_program_manager:
            return TeleworkSignature.objects.filter(application=self, employee=self.employee.get_program_manager, index=0).count()
    
    def division_director_signed(self):
        if self.employee.has_division_director:
            return TeleworkSignature.objects.filter(application=self, employee=self.employee.get_division_director, index=0).count()

    def manager_signature(self):
        signature = TeleworkSignature.objects.filter(application=self, employee=self.employee.manager, index=0).first()
        if signature:
            return[0, "Manager", signature.employee.user.get_full_name(), signature.date, None, False] # Not ready to sign because there is a signature
        else:
            return [0, "Manager", None, None, self.employee.manager.pk, True]
    
    def program_manager_signature(self, index):
        # Rule out this being someone who does not ultimately report to a program manager
        if self.employee.is_division_director:
            return
        if self.employee.is_executive_director:
            return
        if self.employee.manager.is_division_director:
            return
        # TODO: HR people? Others?

        # Start by getting the program manager, which is the direct report of the division director
        current_employee = self.employee
        while True:
            if current_employee.is_executive_director:
                return
            if current_employee.manager.is_division_director:
                program_manager = current_employee
                break
            if current_employee.manager:
                current_employee = current_employee.manager
            else:
                # If we don't get to a division director somehow
                return
        signature = TeleworkSignature.objects.filter(application=self, employee=program_manager, index=index).first()
        if signature:
            return[index, "Program Manager", signature.employee.user.get_full_name(), signature.date, None, False] # Not ready to sign because there is a signature
        else:
            return [index, "Program Manager", None, None, program_manager.pk, True]

    def program_manager_signature_0(self):
        return self.program_manager_signature(0)

    def program_manager_signature_1(self):
        return self.program_manager_signature(1)
    
    def division_director_signature(self):
        # Start by getting the division director
        current_employee = self.employee
        while True:
            if current_employee.is_division_director:
                director = current_employee
                break
            if current_employee.manager:
                current_employee = current_employee.manager
            else:
                # If we don't get to a division director somehow
                return
        signature = TeleworkSignature.objects.filter(application=self, employee=director, index=0).first()
        if signature:
            return[0, "Division Director", signature.employee.user.get_full_name(), signature.date, None, False] # Not ready to sign because there is a signature
        else:
            return [0, "Division Director", None, None, director.pk, True]

class TeleworkSignature(models.Model):
    class Meta:
        verbose_name = _("Telework Signature")
        verbose_name_plural = _("Telework Signatures")

    def __str__(self):
        return f"{self.employee.user.get_full_name()}'s approval of {self.application.employee.user.get_full_name()}'s telework application"

    application = models.ForeignKey("people.TeleworkApplication", verbose_name=_("telework application"), on_delete=models.CASCADE)
    employee = models.ForeignKey("people.Employee", on_delete=models.CASCADE)
    index = models.SmallIntegerField(default=0)
    date = models.DateField(_("signature date"), auto_now=False, auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Mark as ready for signature if it is complete and has employee signatures
        # TODO: Complete

        # Approve if all required signatures are present
        approve_application = False
        applicant = self.application.employee
        all_signatures = self.application.teleworksignature_set.all()
        has_employee_signature_0 = all_signatures.filter(employee=applicant, index=0).exists()
        has_employee_signature_1 = all_signatures.filter(employee=applicant, index=1).exists()
        if has_employee_signature_0 and has_employee_signature_1:
            if applicant.manager:
                has_manager_signature = all_signatures.filter(employee=self.application.employee.manager).exists()
                if has_manager_signature:
                    if applicant.has_program_manager:
                        program_manager = applicant.get_program_manager
                        has_program_manager_signature_0 = all_signatures.filter(employee=program_manager, index=0).exists()
                        has_program_manager_signature_1 = all_signatures.filter(employee=program_manager, index=1).exists()
                        if has_program_manager_signature_0 and has_program_manager_signature_1:
                            if applicant.has_division_director:
                                division_director = applicant.get_division_director
                                has_division_director_signature = all_signatures.filter(employee=division_director).exists()
                                if has_division_director_signature:
                                    # Application has all the required signatures, so approve
                                    approve_application = True
                            else:
                                # Applicant has no division director but all the other required signatures, so approve
                                approve_application = True
                    else:
                        # Applicant has no program manager but all the other required signatures, so approve
                        approve_application = True
            else:
                # Applicant has no manager but all the other required signatures, so approve
                approve_application = True
        
        if approve_application:
            self.application.status = TeleworkApplication.APPROVED
            self.application.save()
