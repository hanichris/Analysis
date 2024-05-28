from pathlib import Path
import json

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

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