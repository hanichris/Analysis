from functools import cmp_to_key
from operator import attrgetter

from django.core.files.uploadedfile import UploadedFile
from pydantic import BaseModel, EmailStr

from .config import cache_results, sync_plans
from .models import Plan, Report, Subscription, User

class PostData(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    title: str
    comment: str

f = attrgetter('status')

def custom_order(a, b):
    if f(a) == 'active' and f(b) == 'active':
        return -1
    if f(a) == 'paused' and f(b) == 'cancelled':
        return -1
    return 0


async def get_plans():
    """Retrieves the billing plans.

    Fetches the plans from the database if they are available. Otherwise, retrieves
    the plans from lemon squeezy and saves them in the database for future use. The
    saved plans are then returned to the caller.
    Returns:
        A list of `Plan` model instances if available. Otherwise, `None`.
    """
    plans = [plan async for plan in Plan.objects.all()]
    if len(plans) == 0:
        plans = await sync_plans()
    return plans

@cache_results(timeout=60)
async def get_user_reports(user: User):
    """Retrives the reports related to a particular user.

    Args:
        user: The user whose reports have been requested.
    Returns:
        list: All the reports of the particular individual.
    """
    return [
        report
        async for report in
        Report.objects.filter(user=user).order_by('-created_at')
    ]
@cache_results(timeout=60)
async def get_user_subscriptions(user: User):
    """Retrieves the subscriptions for a particular user.

    The retrieved subscriptions are ordered based on their status, i.e.
    1. Active Subscriptions
    2. Paused Subscriptions
    3. Cancelled Subscriptions
    Args:
        user: The user whose subscriptions are to be obtained.
    Returns:
        list: All the subscriptions for the given user.
    """
    subs = [
        sub
        async for sub in
        Subscription.objects.filter(user=user).select_related('plan')
    ]
    return sorted(subs, key=cmp_to_key(custom_order))

async def save_report_files(user: User, files: list[UploadedFile]):
    """Saves the report files for a particular user in the database.

    Args:
        user: The user whose report files need to be saved in the database.
        files: a list of report files uploaded to the server for a given user.
    """
    uploaded_files = [ Report(user=user, file=file) for file in files ]
    await Report.objects.abulk_create(uploaded_files)
