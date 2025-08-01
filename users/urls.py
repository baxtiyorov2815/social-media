from django.urls import path
from .views import ProfileSettingsView, ProfilePageView, FollowersPageView, FollowingView, FollowUser

urlpatterns = [
    path("set/general/", ProfileSettingsView.as_view(), name="profile_settings"),
    path("set/followers/<str:username>/", FollowersPageView.as_view(), name="followers"),
    path("set/following/<str:username>/", FollowingView.as_view(), name="following"),
    path("profile/<str:username>/", ProfilePageView.as_view(), name="profile"),
    path("follow/<str:username>/", FollowUser.as_view(), name='follow'),
]