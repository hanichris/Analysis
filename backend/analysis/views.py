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


class IndexView(LoginRequiredMixin, View):
    parents = Path(__file__).parents
    new_path = parents[1].joinpath('static/manifest.json')
    manifest: dict = json.load(new_path.open(encoding='utf-8'))
    access_token = os.getenv('MAPBOX_ACCESS_TOKEN')

    def get(self, request: HttpRequest, *args, **kwargs):
        return render(
            request,
            "analysis/dashboard.html",
            {
                "manifest": self.manifest,
                "access_token": self.access_token,
            }
        )
    
    def post(self, request: HttpRequest, *args, **kwargs):
        print("User: ", end="")
        print(request.user.id) # type: ignore
        print(json.loads(request.body.decode('utf-8')))
        return JsonResponse({'success': True})

class SignUpView(CreateView):
    form_class = UserCreationForm
    model = User
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"