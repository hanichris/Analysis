import os
import json

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request: HttpRequest):
    cur_path = os.path.dirname(__file__)
    new_path = os.path.relpath('..\\static\\manifest.json', cur_path)
    manifest = json.load(open(new_path))
    print(manifest)
    return render(request, "analysis/dashboard.html", )