from django.core.files.uploadedfile import UploadedFile
from pydantic import BaseModel, EmailStr

from .config import cache_results, sync_plans
from .models import Plan, PhoneNumber, Report, User

class PostData(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    title: str
    comment: str

async def get_plans():
    """Retrieves the billing plans.

    Fetches the plans from the database if they are available. Otherwise, retrieves
    the plans from lemon squeezy and saves them in the database for future use. The
    saved plans are then returned to the caller.
    Returns:
        ( list[Plan] | None ): A list of `Plan` model instances if available.
        Otherwise, `None`.
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

async def save_report_files(user: User, files: list[UploadedFile]):
    """Saves the report files for a particular user in the database.

    Args:
        user: The user whose report files need to be saved in the database.
        files: a list of report files uploaded to the server for a given user.
    """
    uploaded_files = [ Report(user=user, file=file) for file in files ]
    await Report.objects.abulk_create(uploaded_files)

async def get_user_phone_number(user: User) -> None | str:
    """Retrieves a user's phone number from the database.

    Args:
        user: The user whose phone number is required.
    Returns:
        ( str | None ): The phone number of interest if found. Otherwise, None.
    """
    try:
        return await PhoneNumber.objects.filter(
            user=user,
            verified=True
        ).values_list('number', flat=True).aget()
    except PhoneNumber.DoesNotExist:
        return None