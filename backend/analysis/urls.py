from django.views.decorators.cache import cache_page
from django.urls import path, re_path

from . import views

app_name = "analysis"
urlpatterns = [
    path("", cache_page(60 * 60)(views.IndexView.as_view()), name="index"),
    path("dashboard/", views.DashboardView.as_view(), name='dashboard'),
    path("users/<uuid:pk>", views.UserProfileView.as_view(), name='profile'),
    path("download/<int:pk>", views.download_file, name="download_file"),
    path("reports/upload", cache_page(60 * 60)(views.UploadReport.as_view()), name='report_upload'),
    path("accounts/signup/", views.SignUpView.as_view(), name='signup'),
    re_path("(about|contact)/", views.IndexView.as_view()),
]
