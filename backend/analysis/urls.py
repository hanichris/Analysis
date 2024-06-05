from django.urls import path

from . import views

app_name = "analysis"
urlpatterns = [
    path("dashboard/", views.IndexView.as_view(), name='dashboard'),
    path("accounts/signup/", views.SignUpView.as_view(), name='signup')
]
