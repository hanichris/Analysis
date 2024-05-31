from pathlib import Path
import json

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import UserCreationForm
from .models import User

# Create your views here.
def index(request: HttpRequest):
    parents = Path(__file__).parents
    new_path = parents[1].joinpath('static/manifest.json')
    manifest: dict = json.load(new_path.open(encoding='utf-8'))
    print(manifest)
    return render(
        request,
        "analysis/dashboard.html",
        {
            'manifest': manifest.get('assets/main.tsx'),
        },
    )

class SignUpView(CreateView):
    form_class = UserCreationForm
    model = User
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"