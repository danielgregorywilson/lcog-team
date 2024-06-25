from django.db import models
from django.utils.translation import gettext_lazy as _

from people.models import Employee


class Role(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    members = models.ManyToManyField(
        Employee, blank=True, related_name='purchase_roles'
    )


class PurchaseCategory(models.Model):
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Purchase categories'

    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    role = models.ForeignKey(
        Role, blank=True, null=True, on_delete=models.SET_NULL
    )


class PurchaseObject(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        PurchaseCategory, blank=True, null=True, on_delete=models.SET_NULL
    )


class PurchaseRequest(models.Model):
    PR_STATUS_REQUESTED = 'requested'
    PR_STATUS_CANCELLED = 'cancelled'
    PR_STATUS_APPROVED = 'approved'
    PR_STATUS_REJECTED = 'rejected'
    PR_STATUS_ORDERED = 'ordered'
    PR_STATUS_RECEIVED = 'received'
    PR_STATUS_COMPLETE = 'complete'
    
    status_choices = (
        (PR_STATUS_REQUESTED, 'Requested'),
        (PR_STATUS_CANCELLED, 'Cancelled'),
        (PR_STATUS_APPROVED, 'Approved'),
        (PR_STATUS_REJECTED, 'Rejected'),
        (PR_STATUS_ORDERED, 'Ordered'),
        (PR_STATUS_RECEIVED, 'Received'),
        (PR_STATUS_COMPLETE, 'Complete')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        Employee, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='purchase_request_created_by',
    )
    updated_by = models.ForeignKey(
        Employee, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='purchase_request_updated_by',
    )
    request_for = models.ForeignKey(
        Employee, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='purchase_request_for',
    )
    purchase_object = models.ForeignKey(
        PurchaseObject, blank=True, null=True, on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    gl_code = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(
        max_length=255, blank=True, null=True, choices=status_choices
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.status = self.PR_STATUS_REQUESTED
        super().save(*args, **kwargs)


class ExpenseBaseModel(models.Model):
    class Meta:
        abstract = True

    STATUS_DRAFT = 'draft'
    STATUS_SUBMITTED = 'submitted'
    STATUS_APPROVER_APPROVED = 'approver_approved'
    STATUS_APPROVER_DENIED = 'approver_denied'
    STATUS_FISCAL_APPROVED = 'fiscal_approved'
    STATUS_FISCAL_DENIED = 'fiscal_denied'
    STATUS_CHOICES = (
        (STATUS_DRAFT, 'Draft'),
        (STATUS_SUBMITTED, 'Submitted'),
        (STATUS_APPROVER_APPROVED, 'Approver Approved'),
        (STATUS_APPROVER_DENIED, 'Approver Denied'),
        (STATUS_FISCAL_APPROVED, 'Fiscal Approved'),
        (STATUS_FISCAL_DENIED, 'Fiscal Denied'),
    )

    status = models.CharField(
        max_length=17, choices=STATUS_CHOICES, default=STATUS_DRAFT
    )


class ExpenseGL(models.Model):
    class Meta:
        ordering = ["pk",]

    expense = models.ForeignKey(
        'Expense', on_delete=models.CASCADE, related_name='gls'
    )
    code = models.CharField(max_length=255, blank=True)
    percent = models.FloatField(blank=True, null=True)
    approver = models.ForeignKey(
        Employee, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='expense_gls'
    )
    approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(blank=True, null=True)
    approver_note = models.TextField(blank=True)


class Expense(ExpenseBaseModel):
    class Meta:
        ordering = ["pk",]

    month = models.ForeignKey(
        'ExpenseMonth', on_delete=models.CASCADE, related_name='expenses'
    )
    name = models.CharField(max_length=255, blank=True)
    date = models.DateField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    description = models.CharField(max_length=511, blank=True)
    vendor = models.CharField(max_length=255, blank=True)
    job = models.CharField(max_length=255, blank=True)
    receipt = models.FileField(
        _("receipt"), upload_to="uploads/expenses", blank=True, null=True
    )
    approved_at = models.DateTimeField(blank=True, null=True)


class ExpenseMonth(ExpenseBaseModel):
    class Meta:
        ordering = ["pk",]
        unique_together = ['purchaser', 'month', 'year']

    def __str__(self):
        return f'{self.month}/{self.year} for {self.purchaser}'
    
    purchaser = models.ForeignKey(
        Employee, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='expense_months',
    )
    month = models.IntegerField()
    year = models.IntegerField()
    approver = models.ForeignKey(
        Employee, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='approver_of_expense_month',
    )
    approved_at = models.DateTimeField(blank=True, null=True)
    submitter_note = models.TextField(blank=True)
    fiscal_note = models.TextField(blank=True)
    card = models.ForeignKey(
        'ExpenseCard', blank=True, null=True, on_delete=models.SET_NULL,
        related_name='expense_months'
    )


class ExpenseCard(models.Model):
    class Meta:
        ordering = ["pk",]
    
    def __str__(self):
        return f'*{self.last4}'

    last4 = models.IntegerField()
    assignee = models.ForeignKey(
        Employee, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='expense_cards'
    )
    shared = models.BooleanField(default=False)


class ExpenseStatement(models.Model):
    class Meta:
        ordering = ["pk",]
    
    card = models.ForeignKey(
        ExpenseCard, on_delete=models.CASCADE, related_name='statements'
    )
    month = models.IntegerField()
    year = models.IntegerField()


class ExpenseStatementItem(models.Model):
    class Meta:
        ordering = ["pk",]

    statement = models.ForeignKey(
        ExpenseStatement, on_delete=models.CASCADE, related_name='items'
    )
    date = models.DateField(_("Transaction Date"))
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
