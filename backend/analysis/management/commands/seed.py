import logging

from asyncio import get_event_loop
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
        loop = get_event_loop()
        loop.run_until_complete(run_seed(options["file"], options["size"]))
        self.stdout.write("done.")


async def clear_data():
    """Deletes all the dummy users from the database."""
    logger.warn("Delete all users with no administrative permissions")
    await User.people.filter(email__icontains="example").adelete()

async def create_users(fake: Faker, num: int = 20):
    for num in range(num):
        fake_email = fake.unique.email()
        fake_pwd = fake.password()
        logger.info(f"{num}-{fake_email}-{fake_pwd}")
        await User.people.acreate_user(
            email=fake_email,
            password=fake_pwd
        )

async def run_seed(fileName: None | str = None, size: int | None = None):
    await clear_data()
    if not fileName:
        fake = Faker()
        if not size:
            await create_users(fake)
        else:
            await create_users(fake, size)
            

