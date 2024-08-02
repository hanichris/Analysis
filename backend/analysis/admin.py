from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Geofield, Comment
from .forms import UserChangeForm, UserCreationForm

# Register your models here.
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("email", "created_at", "is_staff")
    list_filter = ("email", "is_superuser")

    fieldsets = [
        (None, {"fields": ("email", "password")}),
        ("Permissions", {
            "fields": ("is_staff", "is_superuser", "is_active")
        }),
    ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_active"),
            }
        )
    ]

    search_fields = ("email",)
    ordering = ("email",)

admin.site.register(User, UserAdmin)
admin.site.register(Geofield)
admin.site.register(Comment)