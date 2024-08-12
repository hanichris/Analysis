import re
from typing import Any

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _

from .models import User

class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required \
    fields, plus a repeated password.
    """
    email = forms.EmailField(
        label=_("Email address"),
        help_text=_("Email should be a valid email address matching RFC standard"),
        widget=forms.EmailInput(attrs={'placeholder': 'john@email.com'})
    )
    password1 = forms.CharField(
        label=_("Password"),
        min_length=10,
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("email",)
    
    def clean_password1(self):
        password1: str | Any = self.cleaned_data.get("password1")
        pat = re.compile(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!#%*?&])[A-Za-z\d@#$!%*?&]{10,}$"
        )

        if pat.fullmatch(password1) is None:
            raise ValidationError(
                _(
                    """
                    Passwords must have a minimum of ten characters,
                    at least one uppercase letter, one lowercase letter,
                    a number and a special character.
                    """
                )
            )
        
        return password1


    
    def clean_password2(self):
        # Check the two passwords match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match")
        return password2
    
    def clean_email(self):
        pat = re.compile(
            r"[\w!#$%&'*+\/=?`\{\|\}~^\-]+(?:\.[\w!#$%&'*+\/=?`\{\|\}~^\-])*@(?:[a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,6}"
        )
        email: str | Any = self.cleaned_data.get("email")
        if pat.fullmatch(email) is None:
            raise ValidationError(_("The provided email address is not valid."))
        return email

    def save(self, commit=True):
        user: User = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password1"))
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """
    A form for updating users. Includes all the fields on the user,
    but replaces the password field with the admin's disabled password
    hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ("email", "password", "is_staff", "is_superuser")


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MutlipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)
    
    def clean(self, data: Any, initial: Any | None = None) -> Any:
        single_file_clean = super().clean
        if isinstance(data, list | tuple):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class UploadFileForm(forms.Form):
    email = forms.EmailField(
        label=_("Email address"),
        help_text=_("Email should be a valid email address matching RFC standard"),
        widget=forms.EmailInput(attrs={'placeholder': 'john@email.com'})
    )
    file = MutlipleFileField(
        widget=MultipleFileInput(attrs={
            'accept': 'application/pdf, .pdf',
        })
    )

    def clean_email(self):
        pat = re.compile(
            r"[\w!#$%&'*+\/=?`\{\|\}~^\-]+(?:\.[\w!#$%&'*+\/=?`\{\|\}~^\-])*@(?:[a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,6}"
        )
        email: str | Any = self.cleaned_data.get("email")
        if pat.fullmatch(email) is None:
            raise ValidationError(_("The provided email address is not valid."))
        return email