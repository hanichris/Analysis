import logging
import time

from typing import Any

from django.core.management.base import BaseCommand, CommandParser
from faker import Faker

from analysis.models import User

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Seed the database table `user` with user data"
    output_transaction = True
    # missing_args_message = "The filename to the data is missing."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "-f", "--file",
            type=str,
            required=False,
            help="Name of file to use for seeding"
        )

        parser.add_argument(
            "-s", "--size",
            type=int,
            required=False,
            help="Number of users to generate",
        )

    def handle(self, *args: Any, **options: Any) -> str | None:
        self.stdout.write("Seeding data....")
        run_seed(options["file"], options["size"])
        self.stdout.write("done.")


def clear_data():
    """Deletes all the dummy users from the database."""
    logger.warn("Delete all users with no administrative permissions")
    User.people.filter(email__icontains="example").delete()

def create_users(fake: Faker, num: int = 15):
    for num in range(num):
        fake_email = fake.unique.email()
        fake_pwd = fake.password()
        logger.info(f"{num}-{fake_email}-{fake_pwd}")
        User.people.create_user(
            email=fake_email,
            password=fake_pwd
        )

def run_seed(fileName: None | str = None, size: int | None = None):
    clear_data()
    if not fileName:
        fake = Faker()
        if not size:
            create_users(fake)
        else:
            create_users(fake, size)
            

