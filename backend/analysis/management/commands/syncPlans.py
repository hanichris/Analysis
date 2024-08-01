from typing import Any
from django.core.management.base import BaseCommand

from analysis.config import configure_lemonsqueezy
from analysis.models import Plan


class Command(BaseCommand):
    help = "Sync up the data in the Plan db table with LemonSqueezy"

    def handle(self, *args: Any, **options: Any) -> str | None:
        self.stdout.write("Syncing with LemonSqueezy....")
        configure_lemonsqueezy()
        plans = Plan.objects.all()
