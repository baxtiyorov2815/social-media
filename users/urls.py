from django.urls import path
from .views import ProfileSettingsView, ProfilePageView

urlpatterns = [
    path("set/", ProfileSettingsView.as_view(), name="profile_settings"),
    path("profile/", ProfilePageView.as_view(), name="profile"),
]