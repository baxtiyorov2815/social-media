from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .models import UserProfile

User = get_user_model()

# Create your views here.
class ProfileSettingsView(LoginRequiredMixin, View):
    login_url = "/auth/login/"
    template_name = "setting.html"
    
    def get(self, request):
        return render(request=request,
                      template_name=self.template_name)
    
    def post(self, request, *args, **kwargs):
        pass
    
class SigninPageView(View):
    template_name = "signin.html"
    def get(self, req, *args, **kwargs):
        return render(request=req, template_name=self.template_name)

    def post(self, request, *args, **kwargs):
        pass

class SignupPageView(View):
    template_name = "signup.html"

    def get(self, request, *args, **kwargs):
        return render(request=request, template_name=self.template_name)
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.info(request=request, message="Password didnt match!!!")
            return redirect("signup")

        elif User.objects.filter(email=email).exists():
            messages.info(request=request, message=f"{email} already in use!!!")
            return redirect("signup")

        elif User.objects.filter(username=username).exists():
            messages.info(request=request, message=f"{username} already in use!!!")
            return redirect("signup")

        else:
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password1)
            user.save()
            # authenticate(request=request, user=user)
            # login(request=request, user=user)

            # Set profile
            profile = UserProfile.objects.create(user=user)
            print(profile)
            profile.save()

            return redirect("home")