import json
import os
from pathlib import Path

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, View

from .forms import UserCreationForm
from .models import User


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
        return render(
            request,
            "analysis/dashboard.html",
            {
                "access_token": self.access_token,
            }
        )

    def post(self, request: HttpRequest, *args, **kwargs):
        userId = request.user.id #type: ignore
        data = json.loads(request.body.decode('utf-8'))
        print(f"{userId = }")
        for feature in data.features:
            feature.get('id')
        return JsonResponse({'success': True})

class SignUpView(CreateView):
    form_class = UserCreationForm
    model = User
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"