from django.contrib import admin

from .models import (
    Expense, ExpenseMonth, PurchaseCategory, PurchaseObject, PurchaseRequest,
    Role
)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    filter_horizontal = ("members",)


@admin.register(PurchaseCategory)
class PurchaseCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(PurchaseObject)
class PurchaseObjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')


@admin.register(PurchaseRequest)
class PurchaseRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'request_for', 'purchase_object', 'name', 'quantity', 'status'
    )


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'purchaser', 'date', 'name', 'status'
    )


@admin.register(ExpenseMonth)
class ExpenseMonthAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'employee', 'year', 'month', 'status'
    )
    list_filter = ('year', 'status',)