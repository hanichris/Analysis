import asyncio
import hashlib
import hmac
import json
import logging
import os

from asgiref.sync import sync_to_async
from datetime import date
from pathlib import Path
from typing import cast

from django.contrib.auth import aauthenticate, alogin, update_session_auth_hash, aupdate_session_auth_hash # type: ignore
from django.core.paginator import Paginator
from django.core.files.uploadedfile import UploadedFile
from django.db import Error
from django.http import HttpRequest, JsonResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect, aget_object_or_404 # type: ignore
from django.views.generic import View

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from pydantic import BaseModel, EmailStr, ValidationError

from .serialisers import WebhookEventSerializer
from .config import sync_plans, get_checkout_url, webhook_has_meta
from .forms import (
    UserCreationForm,
    UploadFileForm,
    UserEditBirthdayForm,
    UserEditEmailForm,
    UserEditNameForm,
    UserEditPasswordForm,
)
from .mixins import AsyncLoginRequiredMixin, AsyncUserPassesTestMixin
from .models import User, Comment, Report, Plan, WebhookEvent

logger = logging.getLogger(__name__)

class PostData(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    title: str
    comment: str

@api_view(['POST'])
def webhook(request: Request):
    secret = os.getenv('LEMONSQUEEZY_WEBHOOK_SECRET')
    if secret is None:
        return Response(
            'Lemon Squeezy Webhook Secret not set in .env',
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    signature = request.META['HTTP_X_SIGNATURE']
    digest = hmac.new(secret.encode(), request.body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(digest, signature):
        return Response('Invalid signature', status=status.HTTP_400_BAD_REQUEST)
    
    data = request.data
    if webhook_has_meta(data):
        _data = cast(dict, data)
        serializer = WebhookEventSerializer(
            data={'event_name': _data['meta']['event_name'], 'body': _data}
        )
        if serializer.is_valid():
            event = cast(WebhookEvent, serializer.save())
            return Response(status=status.HTTP_200_OK)

    return Response('Invalid data', status=status.HTTP_400_BAD_REQUEST)
    


class IndexView(View):
    parents = Path(__file__).parents
    new_path = parents[1].joinpath('static/manifest.json')
    with new_path.open(encoding='utf-8') as fd:
        manifest: dict = json.load(fd)

    async def get(self, request: HttpRequest, *args, **kwargs):
        return render(
            request,
            "analysis/home.html",
            {
                "manifest": self.manifest.get("src/main.tsx"),
            }
        )
    
    async def post(self, request: HttpRequest, *args, **kwargs):
        try:
            data = PostData(**json.loads(request.body.decode('utf-8')))
            await Comment.objects.acreate(**data.model_dump())
        except ValidationError as err:
            logger.error(err)
            return JsonResponse({
                "msg": "Validation of the data failed.",
                "type": "error",
            }, status_code=400)
        except Error as err:
            logger.error(err)
            return JsonResponse({
                "msg": "An error occurred while saving your message.",
                "type": "error",
            }, status_code=500)
        else:
            return JsonResponse({
                "msg": "Your message has been saved",
                "type": "success"
            }, status=201)

class DashboardView(AsyncLoginRequiredMixin, View):
    
    access_token = os.getenv('MAPBOX_ACCESS_TOKEN')

    async def get(self, request: HttpRequest, *args, **kwargs):
        user = await request.auser() # type: ignore
        return render(
            request,
            "analysis/dashboard.html",
            {
                "access_token": self.access_token,
                "user": user
            }
        )

class SignUpView(View):
    async def get(self, request: HttpRequest, *args, **kwargs):
        form = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})

    async def post(self, request: HttpRequest, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if await sync_to_async(form.is_valid)():
            await sync_to_async(form.save)()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = await aauthenticate(request, email=email, password=password)
            await alogin(request, user)
            return redirect('/billing/')
        return render(
            request, 'registration/signup.html', {'form': form}
        )


# class SignUpView(CreateView):
#     form_class = UserCreationForm
#     model = User
#     success_url = reverse_lazy('login')
#     template_name = "registration/signup.html"


class UserProfileView(AsyncLoginRequiredMixin, View):
    async def get(self, request: HttpRequest, *args, **kwargs):
        user= cast(User, await request.auser()) # type: ignore
        reports =  [
            report
            async for report in 
            Report.objects.filter(user=user).order_by('-created_at')
        ]
        page_number = request.GET.get('page')
        paginator = Paginator(reports, 3)
        page_obj = paginator.get_page(page_number)
        return render(
            request,
            'analysis/profile.html',
            {
                'page_obj': page_obj,
                'user': user,
            }
        )

class UserProfileEditView(AsyncLoginRequiredMixin, View):
    async def get(self, request: HttpRequest, *args, **kwargs):
        user= cast(User, await request.auser()) # type: ignore
        field = request.GET.get('field')
        title = ''
        form = None
        match(field):
            case 'name':
                title = 'name'
                form = UserEditNameForm(initial={
                    'first_name': user.first_name.capitalize() if user.first_name else '',
                    'last_name': user.last_name.capitalize() if user.last_name else '',
                })
            case 'birthday':
                title = 'birthday'
                form = UserEditBirthdayForm(initial={
                    'month': user.birth_date.month if user.birth_date else '',
                    'day': user.birth_date.day if user.birth_date else '',
                    'year': user.birth_date.year if user.birth_date else '',
                })
            case 'email':
                title = 'email'
                form = UserEditEmailForm(initial={'email': user.email})
            case 'password':
                title = 'password'
                form = UserEditPasswordForm()
            case _:
                return HttpResponseNotFound()
        return render(
            request,
            'analysis/edit.html',
            {
                'form': form,
                'title': title,
                'user': user,
            }
        )

    async def post(self, request: HttpRequest, *args, **kwargs):
        user= cast(User, await request.auser()) # type: ignore
        field = request.POST.get('field')
        form = None
        title = ''
        match(field):
            case 'name':
                title = 'name'
                form = UserEditNameForm(request.POST)
            case 'birthday':
                title = 'birthday'
                form = UserEditBirthdayForm(request.POST)
            case 'email':
                title = 'email'
                form = UserEditEmailForm(request.POST)
            case 'password':
                title = 'password'
                form = UserEditPasswordForm(request.POST)
            case _:
                return HttpResponseNotFound()
        
        if form.is_valid():
            match(field):
                case 'name':
                    user.first_name = cast(str, form.cleaned_data['first_name']).lower()
                    user.last_name = cast(str, form.cleaned_data['last_name']).lower()
                case 'birthday':
                    day = form.cleaned_data['day']
                    month = form.cleaned_data['month']
                    year = form.cleaned_data['year']
                    iso_date = f"{year:0>4}-{month:0>2}-{day:0>2}"
                    user.birth_date = date.fromisoformat(iso_date)
                case 'email':
                    user.email = form.cleaned_data['email']
                case 'password':
                    user.set_password(form.cleaned_data['password1'])
                case _:
                    return HttpResponseNotFound()
            await user.asave()
            if field == 'password':
                # Updating the password logs out the current user from existing session.
                # Thus, log them back in. Provided functions do not work as intended.
                await alogin(request, user)
                # await sync_to_async(update_session_auth_hash)(request, user)
                # await aupdate_session_auth_hash(request, user)
        else:
            return render(
                request,
                'analysis/edit.html',
                {
                    'form': form,
                    'title': title,
                    'user': user,
                }
            )
        return HttpResponseRedirect(f'/users/{user.id}/')


class UploadReport(AsyncLoginRequiredMixin, AsyncUserPassesTestMixin, View):
    async def get(self, request: HttpRequest, *args, **kwargs):
        return render(
            request,
            "analysis/upload.html",
            {
                'form': UploadFileForm(),
            }
        )
    
    async def post(self, request: HttpRequest, *args, **kwargs):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = await aget_object_or_404(User, email=email)
            await self.handle_uploaded_file(user, form.cleaned_data['file'])
        else:
            return render(
                request,
                'analysis/upload.html',
                {
                    'form': form
                }
            )
            
        return render(
            request,
            "analysis/upload.html",
            {
                'form': UploadFileForm(),
            }
        )

    async def handle_uploaded_file(self, user: User, files: list[UploadedFile]):
        uploaded_files = [
            Report(
                user=user,
                file=file
            )
            for file in files
        ]

        await Report.objects.abulk_create(uploaded_files)


async def download_file(request, pk: int):
    uploaded_file = await Report.objects.aget(pk=pk)
    print(uploaded_file.file.name)

class Billing(AsyncLoginRequiredMixin, View):
    async def get(self, request: HttpRequest, *args, **kwargs):
        user = await request.auser() # type: ignore
        count = await Plan.objects.acount()
        plans = await sync_plans() if count == 0 else [
            plan async for plan in Plan.objects.all()
        ]
        if plans:
            async with asyncio.TaskGroup() as tg:
                tasks = [
                    tg.create_task(get_checkout_url(plan.variant_id, user))
                    for plan in plans
                ]
            urls = [task.result() for task in tasks]
            plans = zip(plans, urls)
        return render(
            request,
            'analysis/billing.html',
            {
                'plans': plans,
            }
        )
