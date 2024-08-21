import asyncio

from typing import Any, cast
from django.core.management.base import BaseCommand

from analysis.config import sync_plans


class Command(BaseCommand):
    help = "Sync up the data in the Plan db table with LemonSqueezy"

    def handle(self, *args: Any, **options: Any) -> str | None:
        self.stdout.write("Syncing with LemonSqueezy....")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(sync_plans()) 
        self.stdout.write(self.style.SUCCESS("Synchronisation completed successfully"))
