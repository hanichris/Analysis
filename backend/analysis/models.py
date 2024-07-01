import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import Group, Permission, PermissionsMixin
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

# Create your models here.

class AbstractTime(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(PermissionsMixin, AbstractTime, AbstractBaseUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    email = models.EmailField(_('email address'), unique=True, db_index=True)
    name = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group)
    user_permissions = models.ManyToManyField(Permission)


    USERNAME_FIELD="email"
    EMAIL_FIELD="email"
    REQUIRED_FIELDS=[]

    people=CustomUserManager()

    def __str__(self) -> str:
        return self.email
    
class Geofield(AbstractTime):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feature_id = models.UUIDField(null=True, unique=True)
    geometry = models.JSONField(encoder=DjangoJSONEncoder)

    def __str__(self) -> str:
        return f"{
            self.feature_id.hex if self.feature_id else None
        } {self.user} {self.geometry}"

class Message(AbstractTime):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    updated_at = None

    def __str__(self) -> str:
        return f"{self.message[:10]}"
