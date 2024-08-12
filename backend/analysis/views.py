import json
import logging
import os

from pathlib import Path

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import UploadedFile
from django.db import Error, transaction
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, View, DetailView

from pydantic import BaseModel, EmailStr, ValidationError

from .forms import UserCreationForm, UploadFileForm
from .models import User, Comment, Report

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

    def get(self, request: HttpRequest, *args, **kwargs):
        return render(
            request,
            "analysis/home.html",
            {
                "manifest": self.manifest.get("src/main.tsx"),
            }
        )
    
    def post(self, request: HttpRequest, *args, **kwargs):
        try:
            data = PostData(**json.loads(request.body.decode('utf-8')))
            Comment.objects.create(**data.model_dump())
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

class DashboardView(LoginRequiredMixin, View):
    
    access_token = os.getenv('MAPBOX_ACCESS_TOKEN')

    def get(self, request: HttpRequest, *args, **kwargs):
        return render(
            request,
            "analysis/dashboard.html",
            {
                "access_token": self.access_token
            }
        )

class SignUpView(CreateView):
    form_class = UserCreationForm
    model = User
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "analysis/profile.html"

class UploadReport(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, *args, **kwargs):
        return render(
            request,
            "analysis/upload.html",
            {
                'form': UploadFileForm(),
            }
        )
    
    def post(self, request: HttpRequest, *args, **kwargs):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            email = request.POST['email']
            user = get_object_or_404(User, email=email)
            self.handle_uploaded_file(user, form.cleaned_data['file'])
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

    def handle_uploaded_file(self, user: User, files: list[UploadedFile]):
        uploaded_files = [
            Report(
                user=user,
                file=file
            )
            for file in files
        ]

        with transaction.atomic():
            Report.objects.bulk_create(uploaded_files)
