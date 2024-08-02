from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, /, *, email: str, password: str, **kwargs):
        """
        Create and save a user with the given email and password.

        Args:
            email: str
            password: str

        Raises:
            ValueError

        Return:
            user instance.
        """
        if not email:
            raise ValueError(_("Users must have an email address"))

        if not password:
            raise ValueError(_("Users must have a password"))

        user = self.model(
            email=self.normalize_email(email),
            **kwargs
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str, **kwargs):
        """
        Create and save a superuser with the given email and password.

        Args:
            email: str
            password: str

        Return:
            user instance
        """
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)

        if kwargs.get('is_staff') is not True:
            raise ValueError(_("Superuser must have 'is_staff'=True"))
        if kwargs.get('is_superuser') is not True:
            raise ValueError(_("Superuser must have 'is_superuser'=True"))

        return self.create_user(
            email=email,
            password=password,
            **kwargs
        )
    
    async def acreate_user(self, /, *,  email: str, password: str, **kwargs):
        """
        Create and save a user with the given email and password.

        The method is an asynchronous version of the `create_user` method
        that has use in the `management` module.

        Args:
            email: str
            password: str

        Return:
            user instance.

        Raises:
            ValueError
        """
        if not email:
            raise ValueError(_("Users must have an email address"))

        if not password:
            raise ValueError(_("Users must have a password"))

        user = self.model(
            email=self.normalize_email(email),
            **kwargs
        )
        user.set_password(password)
        await user.asave()
        return user

    async def acreate_superuser(self, email: str, password: str, **kwargs):
        """
        Create and save a superuser with the given email and password.

        The method is an asynchronous version of the `create_superuser` method.
        Args:
            email: str
            password: str

        Return:
            user instance
        """
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)

        if kwargs.get('is_staff') is not True:
            raise ValueError(_("Superuser must have 'is_staff'=True"))
        if kwargs.get('is_superuser') is not True:
            raise ValueError(_("Superuser must have 'is_superuser'=True"))

        return await self.acreate_user(
            email=email,
            password=password,
            **kwargs
        )
