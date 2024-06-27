import json
import logging
import os

from uuid import UUID
from pathlib import Path

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError, transaction
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, View

from .forms import UserCreationForm
from .models import User, Geofield

logger = logging.getLogger(__name__)

class IndexView(View):
    parents = Path(__file__).parents
    new_path = parents[1].joinpath('static/manifest.json')
    manifest: dict = json.load(new_path.open(encoding='utf-8'))

    def get(self, request: HttpRequest, *args, **kwargs):
        return render(
            request,
            "analysis/home.html",
            {
                "manifest": self.manifest.get("assets/main.tsx"),
            }
        )

class DashboardView(LoginRequiredMixin, View):
    
    access_token = os.getenv('MAPBOX_ACCESS_TOKEN')

    def get(self, request: HttpRequest, *args, **kwargs):
        queryset = Geofield.objects.select_related(
            "user"
        ).filter(
            user__email=request.user
        )
        data = [entry for entry in queryset]
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
                id=UUID(feature.get("id")),
                geometry=feature.get("geometry")
            )
            for feature in data.get("features")
        ]

        try:
            with transaction.atomic():
                Geofield.objects.bulk_create(create_data)
        except IntegrityError:
            logger.error(f"sqlite3.IntegrityError: UNIQUE constraint failed")
            return JsonResponse({'error': True}, status=500)

        return JsonResponse({'success': True})

class SignUpView(CreateView):
    form_class = UserCreationForm
    model = User
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"