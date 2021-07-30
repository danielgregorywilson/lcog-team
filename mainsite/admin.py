from django import forms
from django.contrib import admin
from django.contrib.auth import password_validation
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _


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