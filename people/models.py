import datetime

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

SHOW_REVIEW_TO_MANAGER_DAYS_BEFORE_DUE = 60


class Employee(models.Model):
    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("employee_detail", kwargs={"pk": self.pk})

    def username(self):
        return self.user.username

    user = models.OneToOneField("auth.User", verbose_name=_("user"), on_delete=models.CASCADE)
    manager = models.ForeignKey("self", related_name="direct_reports", blank=True, null=True, verbose_name=_("manager"), on_delete=models.CASCADE)
    hire_date = models.DateField(_("hire date"), auto_now=False, auto_now_add=False)
    salary = models.PositiveIntegerField(_("salary"))

    def employee_next_review(self):
        return self.performancereview_set.all().order_by("date").first()

    def get_direct_reports(self):
        return self.direct_reports.all()
    
    def get_direct_reports_descendants(self):
        direct_reports_descendants = []
        for direct_report in self.get_direct_reports():
            for descendant in direct_report.direct_reports.all():
                direct_reports_descendants.append(descendant.pk)
        unique_descendant_pks = list(set(direct_reports_descendants))
        return Employee.objects.filter(pk__in=unique_descendant_pks)

    def manager_upcoming_reviews(self):
        reviews = []
        for employee in self.get_direct_reports():
            employee_reviews = employee.performancereview_set.all()
            for review in employee_reviews:
                if review.days_until_due() < SHOW_REVIEW_TO_MANAGER_DAYS_BEFORE_DUE:
                    reviews.append(review)
        return sorted(reviews, key=lambda review: review.date)
    
    def manager_upcoming_reviews_action_required(self):
        reviews = []
        for review in self.manager_upcoming_reviews():
            if any([
                review.status == PerformanceReview.NEEDS_EVALUATION,
                review.status == PerformanceReview.EVALUATION_WRITTEN_AND_DATE_SET and not review.performanceevaluation.manager_discussed,
                review.status == PerformanceReview.EVALUATION_DENIED
            ]):
                reviews.append(review)
        return reviews
    
    def manager_upcoming_reviews_no_action_required(self):
        reviews = []
        for review in self.manager_upcoming_reviews():
            if any([
                review.status == PerformanceReview.EVALUATION_WRITTEN_AND_DATE_SET and review.performanceevaluation.manager_discussed,
                review.status == PerformanceReview.EVALUATION_COMPLETED,
                review.status == PerformanceReview.EVALUATION_APPROVED
            ]):
                reviews.append(review)
        return reviews

    def upper_manager_upcoming_reviews(self):
        reviews = []
        for employee in self.get_direct_reports_descendants():
            employee_reviews = employee.performancereview_set.all()
            for review in employee_reviews:
                if review.days_until_due() < SHOW_REVIEW_TO_MANAGER_DAYS_BEFORE_DUE:
                    reviews.append(review)
        return sorted(reviews, key=lambda review: review.date)
    
    def upper_manager_upcoming_reviews_action_required(self):
        reviews = []
        for review in self.upper_manager_upcoming_reviews():
            if any([
                review.status == PerformanceReview.EVALUATION_COMPLETED
            ]):
                reviews.append(review)
        return reviews
    
    def upper_manager_upcoming_reviews_no_action_required(self):
        reviews = []
        for review in self.upper_manager_upcoming_reviews():
            if any([
                review.status == PerformanceReview.NEEDS_EVALUATION,
                review.status == PerformanceReview.EVALUATION_WRITTEN_AND_DATE_SET,
                review.status == PerformanceReview.EVALUATION_DENIED,
                review.status == PerformanceReview.EVALUATION_APPROVED
            ]):
                reviews.append(review)
        return reviews



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


class UpperManagerUpcomingReviewsActionRequiredManager(models.Manager):
    def get_queryset(self, user):
        queryset = super().get_queryset()
        desired_pks = [pr.pk for pr in user.employee.upper_manager_upcoming_reviews_action_required()]
        queryset = queryset.filter(pk__in=desired_pks)
        return queryset


class UpperManagerUpcomingReviewsNoActionRequiredManager(models.Manager):
    def get_queryset(self, user):
        queryset = super().get_queryset()
        desired_pks = [pr.pk for pr in user.employee.upper_manager_upcoming_reviews_no_action_required()]
        queryset = queryset.filter(pk__in=desired_pks)
        return queryset


class PerformanceReview(models.Model):
    class Meta:
        verbose_name = _("Performance Review")
        verbose_name_plural = _("Performance Reviews")

    def __str__(self):
        return f"Performance review for {self.employee.user.username} on {self.date}"

    def get_absolute_url(self):
        return reverse("performance_review_detail", kwargs={"pk": self.pk})

    # Managers for filtering PRs
    objects = models.Manager()
    manager_upcoming_reviews_action_required = ManagerUpcomingReviewsActionRequiredManager()
    manager_upcoming_reviews_no_action_required = ManagerUpcomingReviewsNoActionRequiredManager()
    upper_manager_upcoming_reviews_action_required = UpperManagerUpcomingReviewsActionRequiredManager()
    upper_manager_upcoming_reviews_no_action_required = UpperManagerUpcomingReviewsNoActionRequiredManager()

    NEEDS_EVALUATION = 'N'
    EVALUATION_WRITTEN_AND_DATE_SET = 'EW'
    EVALUATION_COMPLETED = 'EC'
    EVALUATION_DENIED = 'ED'
    EVALUATION_APPROVED = 'EA'
    EVALUATION_HR_PROCESSED = 'EP'
    STATUS_CHOICE = [
        (NEEDS_EVALUATION, 'Needs evaluation'),
        (EVALUATION_WRITTEN_AND_DATE_SET, 'Evaluation written and date for discussion set'),
        (EVALUATION_COMPLETED, 'Evaluation discussed with employee'),
        (EVALUATION_DENIED, 'Evaluation denied'),
        (EVALUATION_APPROVED, 'Evaluation approved'),
        (EVALUATION_HR_PROCESSED, 'Evaluation processed by HR'),
    ]
    employee = models.ForeignKey("Employee", verbose_name=_("employee"), on_delete=models.CASCADE)
    date = models.DateField(_("review date"), auto_now=False, auto_now_add=False)
    status = models.CharField(_("review status"), max_length=2, choices=STATUS_CHOICE, default=NEEDS_EVALUATION)

    def username(self):
        return self.employee.user.username

    def days_until_due(self):
        timedelta = self.date - datetime.date.today()
        return timedelta.days

    def overdue(self):
        if self.days_until_due() <= 0:
            return True
        return False


class PerformanceEvaluation(models.Model):
    class Meta:
        verbose_name = _("Performance Evaluation")
        verbose_name_plural = _("Performance Evaluations")

    def get_absolute_url(self):
        return reverse("performance_evaluation_detail", kwargs={"pk": self.pk})
    
    review = models.OneToOneField("people.PerformanceReview", verbose_name=_("performance review"), on_delete=models.CASCADE)
    evaluation = models.TextField(_("performance evaluation"), blank=True, null=True)
    discussion_date = models.DateField(_("discussion date"), auto_now=False, auto_now_add=False, blank=True, null=True)
    employee_discussed = models.BooleanField(_("employee discussed the evaluation"), default=False)
    manager_discussed = models.BooleanField(_("manager discussed the evaluation"), default=False)
    upper_manager_accepted = models.BooleanField(_("upper manager accepted the evaluation"), default=False)
    upper_manager_note = models.TextField(_("upper manager note"), default="", blank=True, null=True)


class ReviewNote(models.Model):
    class Meta:
        verbose_name = _("Performance Review Note")
        verbose_name_plural = _("Performance Review Notes")

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