import json
import logging
import os

from uuid import UUID
from pathlib import Path

from django.core import serializers
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, View, DetailView

from pydantic import BaseModel, EmailStr, ValidationError

from .forms import UserCreationForm
from .models import User, Geofield, Comment

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
    manifest: dict = json.load(new_path.open(encoding='utf-8'))

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
                "error": "Validation of the data failed."
            }, status_code=500)

        return JsonResponse({
            "success": "comment has been created",
            "error": None
        })

class DashboardView(LoginRequiredMixin, View):
    
    access_token = os.getenv('MAPBOX_ACCESS_TOKEN')

    def get(self, request: HttpRequest, *args, **kwargs):
        queryset = Geofield.objects.select_related(
            "user"
        ).filter(
            user__email=request.user
        )
        data = [(entry.feature_id, entry.geometry) for entry in queryset]
        return render(
            request,
            "analysis/dashboard.html",
            {
                "access_token": self.access_token,
            }
        )

    def post(self, request: HttpRequest, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        create_data = [
            Geofield(
                user=request.user,
                feature_id=UUID(feature.get("id")),
                geometry=feature.get("geometry")
            )
            for feature in data.get("features")
        ]

        with transaction.atomic():
            objs = serializers.serialize(
                'json',
                Geofield.objects.bulk_create(
                    create_data,
                    ignore_conflicts=True
                )
            )

        return JsonResponse({'success': True, "data": objs})

class SignUpView(CreateView):
    form_class = UserCreationForm
    model = User
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"


class UserProfileView(DetailView):
    model = User
    template_name = "analysis/profile.html"