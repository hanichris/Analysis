import logging

import asyncio
from itertools import islice
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
            "-b", "--batch",
            type=int,
            required=False,
            help="Create the users in batches.",
        )

        parser.add_argument(
            "-s", "--size",
            type=int,
            required=False,
            help="Number of users to generate",
        )

    def handle(self, *args: Any, **options: Any) -> str | None:
        self.stdout.write("Seeding data....")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            run_seed(
                batch=options['batch'],
                fileName=options['file'],
                size=options['size']
            )
        )
        self.stdout.write("done.")


async def clear_data():
    """Deletes all the dummy users from the database."""
    logger.warn("Delete all users with no administrative permissions")
    await User.people.filter(email__icontains="example").adelete()

async def create_users(batch_size: int = 999, num: int = 20):
    users = (user for user in generate_user(num))
    background_tasks = set()
    batch_size = batch_size if 0 < batch_size < 1000 else 999
    while batch := list(islice(users, batch_size)):
        task = asyncio.create_task(
            User.people.abulk_create(batch, batch_size)
        )
        background_tasks.add(task)
        task.add_done_callback(background_tasks.discard)

    await asyncio.gather(*background_tasks)

async def run_seed(
        *,
        batch: int | None = None,
        fileName: None | str = None,
        size: int | None = None,
):
    await clear_data()
    if not fileName:
        if not size and not batch:
            await create_users()
        elif size and not batch:
            await create_users(num=size)
        elif batch and not size:
            await create_users(batch_size=batch)
        elif batch and size:
            await create_users(batch_size=batch, num=size)

def generate_user(stop: int):
    fake = Faker(use_weighting=False)
    start = 0
    while start < stop:
        user = User(email=fake.unique.email())
        user.set_password(fake.password())
        yield user
        start += 1