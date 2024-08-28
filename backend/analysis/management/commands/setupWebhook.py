import asyncio

from typing import Any
from django.core.management.base import BaseCommand

from analysis.config import setup_webhook


class Command(BaseCommand):
    help = "Set up a webhook on Lemon Squeezy store."

    def handle(self, *args: Any, **options: Any):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(setup_webhook())