from django.urls import path, re_path

from . import views

app_name = "analysis"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("dashboard/", views.DashboardView.as_view(), name='dashboard'),
    path("users/<uuid:pk>", views.UserProfileView.as_view(), name='profile'),
    path("accounts/signup/", views.SignUpView.as_view(), name='signup'),
    re_path("(about|contact)/", views.IndexView.as_view()),
]
