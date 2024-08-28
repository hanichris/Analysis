import asyncio
import json
import logging
import os

from asgiref.sync import sync_to_async
from pathlib import Path
from typing import cast

from django.contrib.auth import aauthenticate, alogin
from django.core.paginator import Paginator
from django.core.files.uploadedfile import UploadedFile
from django.db import Error
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect, aget_object_or_404 # type: ignore
from django.views.generic import View

from pydantic import BaseModel, EmailStr, ValidationError

from .config import sync_plans, get_checkout_url
from .forms import UserCreationForm, UploadFileForm
from .mixins import AsyncLoginRequiredMixin, AsyncUserPassesTestMixin
from .models import User, Comment, Report, Plan

logger = logging.getLogger(__name__)

class PostData(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    title: str
    comment: str

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
    async def post(self, *args, **kwargs):
        pass

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

        async with asyncio.TaskGroup() as tg:
            tasks = [
                tg.create_task(get_checkout_url(plan.variant_id, user))
                for plan in cast(list[Plan], plans)
            ]
        urls = [task.result() for task in tasks]
        return render(
            request,
            'analysis/billing.html',
            {
                'plans': zip(cast(list[Plan], plans), urls),
            }
        )

    async def post(self, request: HttpRequest, *args, **kwargs):
        pass
