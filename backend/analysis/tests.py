from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from .models import User as UserClass


# Create your tests here.
class UserManagersTests(TestCase):
    def test_create_user(self):
        """
        create_user() inserts a new user in the database with the following \
        attributes: `email`, `password`, `is_active=True`, `is_staff=False`, \
        `is_superuser=False` and `name=null`.
        """
        User = get_user_model()
        user: UserClass = User.people.create_user( # type: ignore
            email="normal@user.com",
            password="foo",
        )
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsNone(user.name)

        with self.assertRaises(TypeError):
            User.people.create_user() # type: ignore
        with self.assertRaises(TypeError):
            User.people.create_user(email="") # type: ignore
        with self.assertRaises(ValueError):
            User.people.create_user(email="", password="foo") # type: ignore
        with self.assertRaises(ValueError):
            User.people.create_user(email="test@test.com", password="") # type: ignore
    
    def test_create_superuser(self):
        """
        create_superuser() inserts a new user in the database with the following \
        attributes: `email`, `password`, `isactive=True`, `is_staff=True`,
        `is_superuser=True` and `name=null`
        """
        User = get_user_model()
        admin_user: UserClass = User.people.create_superuser( # type: ignore
            email="super@user.com",
            password="bar"
        )
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertIsNone(admin_user.name)

        with self.assertRaises(ValueError):
            User.people.create_superuser( # type: ignore
                email="super@user.com",
                password="bar",
                is_staff=False
            )
        with self.assertRaises(ValueError):
            User.people.create_superuser( # type: ignore
                email="super@user.com",
                password="bar",
                is_superuser=False
            )
        

class SyncPlansTest(TestCase):
    def test_command_operation_syncPlans(self):
        out = StringIO()
        call_command("syncPlans", stdout=out)
        self.assertRaises(ValueError)