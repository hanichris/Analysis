from django.http import Http404, HttpRequest
from django.shortcuts import render

# Create your views here.
def index(request: HttpRequest):
    raise Http404("What you are looking for is not here.")