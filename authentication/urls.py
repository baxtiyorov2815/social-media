from django.urls import path
from .views import SigninPageView, SignupPageView, LogoutPageView, EmailVerificationPageView

urlpatterns = [
    path("login/", SigninPageView.as_view(), name="login"),
    path("signup/", SignupPageView.as_view(), name="signup"),
    path("logout/", LogoutPageView.as_view(), name="logout"),
    path("verify-email/<str:username>/", EmailVerificationPageView.as_view(), name="verify-email"),
]