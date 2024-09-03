import re
from typing import Any, cast

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _

from .models import User

MONTH_CHOICES = {
    1: _('January'),
    2: _('February'),
    3: _('March'),
    4: _('April'),
    5: _('May'),
    6: _('June'),
    7: _('July'),
    8: _('August'),
    9: _('September'),
    10: _('October'),
    11: _('November'),
    12: _('December'),
}


def validate_integer(value):
    try:
        int(value)
    except ValueError:
        raise ValidationError(
            _("%(value)s is not a valid number"),
            params={'value': value},
            code="invalid field"
        )

def validate_range(value):
    try:
        x = int(value)
        if x > 31 or x < 1:
            raise ValidationError(
                _("%(value)s is not within the valid day range"),
                code="invalid day",
                params={'value': value},
            )
    except ValueError:
        raise ValidationError(
            _("%(value)s is not a valid number"),
            params={'value': value},
            code="invalid field"
        )

def is_leap_year(year: int) -> bool:
    year = int(year)
    return year % 400 == 0 or ((year % 4 == 0) and (year % 100 != 0))

def has_31_days(month: int) -> bool:
    month = int(month)
    return month in {1, 3, 5, 7, 8, 10, 12}

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
                ),
                code="invalid password"
            )
        
        return password1


    
    def clean_password2(self):
        # Check the two passwords match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError(
                _("Passwords do not match"),
                code="mismatched passwords"
            )
        return password2
    
    def clean_email(self):
        pat = re.compile(
            r"[\w!#$%&'*+\/=?`\{\|\}~^\-]+(?:\.[\w!#$%&'*+\/=?`\{\|\}~^\-])*@(?:[a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,6}"
        )
        email: str | Any = self.cleaned_data.get("email")
        if pat.fullmatch(email) is None:
            raise ValidationError(
                _("The provided email address is not valid."),
                code="invalid email"
            )
        return email.lower()

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
            raise ValidationError(
                _("The provided email address is not valid."),
                code="invalid email"
            )
        return email.lower()
    

class UserEditEmailForm(forms.Form):
    email = forms.EmailField(
        label=_("Email address"),
        help_text=_("Email should be a valid email address matching RFC standard"),
        widget=forms.EmailInput(attrs={'placeholder': 'john@email.com'})
    )

    def clean_email(self):
        pat = re.compile(
            r"[\w!#$%&'*+\/=?`\{\|\}~^\-]+(?:\.[\w!#$%&'*+\/=?`\{\|\}~^\-])*@(?:[a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,6}"
        )
        email: str | Any = self.cleaned_data.get("email")
        if pat.fullmatch(email) is None:
            raise ValidationError(
                _("The provided email address is not valid."),
                code="invalid email"
            )
        return email.lower()

class UserEditPasswordForm(forms.Form):
    password1 = forms.CharField(
        label=_("Password"),
        min_length=10,
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput
    )

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
                ),
                code="invalid password"
            )
        
        return password1

    def clean_password2(self):
        # Check the two passwords match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError(
                _("Passwords do not match"),
                code='mismatched passwords'
            )
        return password2

class UserEditNameForm(forms.Form):
    first_name = forms.CharField(
        label=_('First name'),
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Kgauhelo'})
    )
    last_name = forms.CharField(
        label=_('Last name'),
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'José'})
    )


class UserEditBirthdayForm(forms.Form):
    month = forms.TypedChoiceField(
        coerce=int,
        choices=MONTH_CHOICES,
        label=_('month')
    )
    day = forms.CharField(
        label=_('day'),
        max_length=2,
        min_length=1,
        validators=[validate_integer, validate_range],
        widget=forms.TextInput(attrs={'placeholder': 'DD'})
    )
    year = forms.CharField(
        label=_('year'),
        max_length=4,
        min_length=4,
        validators=[validate_integer],
        widget=forms.TextInput(attrs={'placeholder': 'YYYY'})
    )

    def clean(self):
        super().clean()
        month = self.cleaned_data.get('month')
        day = self.cleaned_data.get('day')
        year = self.cleaned_data.get('year')

        if day and month and year:
            day = int(day)
            if not is_leap_year(year) and month == 2 and day > 28:
                raise ValidationError(
                    _("Enter a valid birthday"),
                    code="invalid day"
                )

            if is_leap_year(year) and month == 2 and day > 29:
                raise ValidationError(
                    _("Enter a valid birthday"),
                    code="invalid day"
                )
            
            if not has_31_days(month) and day > 30:
                raise ValidationError(
                    _("Enter a valid birthday"),
                    code="invalid day"
                )