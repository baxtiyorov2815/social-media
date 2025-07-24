from django.urls import path
from .views import ProfileSettingsView, SigninPageView, SignupPageView

urlpatterns = [
    path("set/", ProfileSettingsView.as_view(), name="profile"),
    path("login/", SigninPageView.as_view(), name="login"),
    path("signup/", SignupPageView.as_view(), name="signup"),
]