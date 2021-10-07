from mainsite.models import ImageUpload, SecurityMessage
from django import forms
from django.contrib import admin
from django.contrib.auth import password_validation
from django.contrib.auth.admin import GroupAdmin, UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth.models import Group, User
from django.utils.translation import gettext, gettext_lazy as _

from mainsite.models import ImageUpload, SecurityMessage


@admin.register(ImageUpload)
class ImageUploadAdmin(admin.ModelAdmin):
    list_display = ("pk", "description")


@admin.register(SecurityMessage)
class SecurityMessageAdmin(admin.ModelAdmin):
    list_display = ("description", "date", "active")



class UserCreationForm(BaseUserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
        required=False
    )


# admin.site.unregister(User)

# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     add_form = UserCreationForm


admin.site.unregister(Group)
class UserInLine(admin.TabularInline):
    model = Group.user_set.through
    extra = 0


@admin.register(Group)
class GenericGroup(GroupAdmin):
    inlines = [UserInLine]