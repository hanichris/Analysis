from django.views.decorators.cache import cache_page
from django.urls import path, re_path, include

from . import views

app_name = "analysis"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("api/webhook", views.webhook, name='lswhk_endpoint'),
    path("custom_urls/<lemonsqueezy_id>", views.retrieve_urls, name='urls'),
    path("pause_subscription/<lemonsqueezy_id>", views.pause_subscription, name='pause_sub'),
    path("resume_subscription/<lemonsqueezy_id>", views.resume_subscription, name='resume_sub'),
    path("cancel_subscription/<lemonsqueezy_id>", views.cancel_subscription, name='cancel_sub'),
    path("billing/", views.Billing.as_view(), name="billing"),
    path("change_plan/<int:pk>", views.ChangeBilling.as_view(), name='change_plan'),
    path("dashboard/", views.DashboardView.as_view(), name='dashboard'),
    path("sw/", views.service_worker, name='service_worker'),
    path("users/<int:pk>/", include(
        [
            path("", views.UserProfileView.as_view(), name='profile'),
            path("coordinates", views.Coordinates.as_view(), name="user_coords"),
            path("edit/", views.UserProfileEditView.as_view(), name='edit_profile'),
        ]
    )),
    path("download/<int:pk>/", views.download_file, name="download_file"),
    path("reports/upload", views.UploadReport.as_view(), name='report_upload'),
    path("accounts/signup/", views.SignUpView.as_view(), name='signup'),
    re_path("(about|contact)/", views.IndexView.as_view()),
]
