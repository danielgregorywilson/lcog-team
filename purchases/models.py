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


class Expense(models.Model):

    class Meta:
        ordering = ["pk",]

    name = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    job = models.CharField(max_length=255, blank=True, null=True)
    gls = models.JSONField(blank=True, null=True)
    purchaser = models.ForeignKey(
        Employee, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='expenses_purchased',
    )
    approver = models.ForeignKey(
        Employee, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='approver_of_expenses',
    )
    approval_notes = models.TextField(blank=True, null=True)
    receipt = models.FileField(_("receipt"), upload_to="uploads/expenses", blank=True, null=True)