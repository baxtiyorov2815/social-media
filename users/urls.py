from django.urls import path
from .views import ProfileSettingsView

urlpatterns = [
    path("set/", ProfileSettingsView.as_view(), name="profile"),
]