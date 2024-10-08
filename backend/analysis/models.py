import uuid

from datetime import date

from django.db import models
from django.db.models.functions import Concat
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import Group, Permission, PermissionsMixin
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

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
    email = models.EmailField(_('email address'), unique=True)
    verified = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    birth_date = models.DateField(null=True)
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
    
    @property
    def full_name(self):
        if self.first_name and self.last_name:
            name = f"{self.first_name} {self.last_name}"
            return name.title()
        elif self.first_name:
            return self.first_name.capitalize()
        elif self.last_name:
            return self.last_name.capitalize()
        return ""
    
    @property
    def age(self):
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - (
                (today.month, today.day) <
                (self.birth_date.month, self.birth_date.day)
            )
        return None
    
    class Meta:
        indexes = [
            models.Index(fields=['id', 'email']),
            models.Index(
                fields=['email'],
                name='unique_verified_email',
                condition=models.Q(verified=True)
            ),
        ]

class PhoneNumber(AbstractTime):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = PhoneNumberField()
    verified = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['number', 'user']),
            models.Index(
                fields=['number'],
                name='verified_number',
                condition=models.Q(verified=True)
            ),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['number', 'user'],
                name='unique_verfified_number',
                condition=models.Q(verified=True)
            ),
        ]

class Geofield(AbstractTime):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feature_id = models.TextField()
    unique_id = models.GeneratedField( # type: ignore
        expression=Concat("user", models.Value(','), "feature_id"),
        output_field=models.TextField(),
        db_persist=True,
        verbose_name="Unique Feature ID",
        unique=True,
    )
    geometry = models.JSONField(encoder=DjangoJSONEncoder)

    def __str__(self) -> str:
        return f"{self.feature_id} {self.user} {self.geometry}"

class Message(AbstractTime):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    updated_at = None

    def __str__(self) -> str:
        return f"{self.message[:10]}"

class Report(AbstractTime):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='pdfs')
    updated_at = None

    class Meta:
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["file"])
        ]
    
    def __str__(self) -> str:
        return self.file.url
    
    @property
    def name(self):
        return self.file.name.rsplit('/', maxsplit=1)[-1]

class Comment(AbstractTime):
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(max_length=55, db_index=True)
    title = models.CharField(max_length=75)
    comment = models.TextField()
    updated_at = None

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return f"Name: `{self.full_name}` Title: `{self.title}` Comment: `{self.comment[:10]}...`"

class Plan(AbstractTime):
    product_id = models.IntegerField()
    product_name = models.TextField(default='')
    variant_id = models.IntegerField(unique=True)
    name = models.TextField()
    description = models.TextField(default='')
    price = models.TextField()
    is_usage_based = models.BooleanField(default=False)
    interval = models.TextField(default='')
    interval_count = models.IntegerField(null=True)
    trial_interval = models.TextField(default='')
    trial_interval_count = models.IntegerField(null=True)
    sort = models.IntegerField(null=True)

    def __str__(self) -> str:
        return f"{self.name} {self.price}"
    
    class Meta:
        indexes = [
            models.Index(fields=["variant_id","name"]),
            models.Index(fields=["variant_id"]),
        ]

class WebhookEvent(AbstractTime):
    event_name = models.TextField()
    processed = models.BooleanField(default=False)
    processing_error = models.TextField(default='')
    body = models.JSONField(encoder=DjangoJSONEncoder)

class Subscription(AbstractTime):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    lemonsqueezy_id = models.TextField(unique=True)
    order_id = models.IntegerField()
    name = models.TextField(default='')
    email = models.EmailField(_('email address'))
    status = models.TextField()
    status_formatted = models.TextField()
    renews_at = models.TextField(default='')
    ends_at = models.TextField(default='')
    trial_ends_at = models.TextField(default='')
    price = models.TextField()
    is_usage_based = models.BooleanField(default=False)
    is_paused = models.BooleanField(default=False)
    subscription_item_id = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=["lemonsqueezy_id"]),
        ]