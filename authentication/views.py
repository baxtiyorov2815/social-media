import random
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from users.models import UserProfile
from django.core.validators import validate_email
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()

# Create your views here.
    
class SigninPageView(View):

    template_name = "authentication/signin.html"

    def is_email(self, value):
        try:
            validate_email(value=value)
            return True
        except:
            return False

    def get(self, req, *args, **kwargs):
        return render(request=req, template_name=self.template_name)

    def post(self, request, *args, **kwargs):
        username_or_email = request.POST.get("username_or_email")
        password = request.POST.get("password")
        if self.is_email(username_or_email):
            user=User.objects.get(email=username_or_email)
            username = user.username
            user = authenticate(username=username, password=password)
            if user is None:
                messages.error(request=request, message="Email or password is wrong!!!")
                return redirect("login")
        else:
            user = authenticate(username=username_or_email, password=password)
            if user is None:
                messages.error(request=request, message="Username or password is wrong!!!")
                return redirect("login")
        login(request=request, user=user)
        return redirect("home")


class SignupPageView(View):
    template_name = "authentication/signup.html"

    def get(self, request, *args, **kwargs):
        return render(request=request, template_name=self.template_name)
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        aggrement = request.POST.get("agreement")

        # genrerate code for email
        code = random.randint(100000, 999999)
        
        if aggrement == "on":
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
                address = email
                subject = "Email Verification for SOCOL"
                message = f"Your verification code: {code}"
                try:
                    send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=[address])
                    messages.success(request=request, message="Verification code sent succesfully!!!")
                except:
                    messages.error(request=request, message="Something went wrong please try again!!!")
                user = User.objects.create_user(username=username,
                                                email=email,
                                                password=password1,
                                                verification_code=code)
                user.is_active = False
                user.save()
                authenticate(request=request, user=user)
                login(request=request, user=user)

                return redirect(to="verify-email", username=username)
        else:
            messages.error(request=request, message="You should agree terms!!!")
            return redirect("signup")       


class LogoutPageView(View):
    def get(self, request, *args, **kwargs):
        logout(request=request)
        return redirect("login")
    
    def post(self, request, *args, **kwargs):
        pass

class EmailVerificationPageView(View):
    template_name = "authentication/verify_email.html"

    def get(self, request, username, *args, **kwargs):
        user = User.objects.get(username=username)
        email = user.email
        return render(request=request, template_name=self.template_name, context={"email": email})
    
    def post(self, request, username, *args, **kwargs):
        user = User.objects.get(username=username)
        code = request.POST.get("ver-code")
        if str(user.verification_code) == str(code):
            # activate user
            user.is_active = True
            user.save()
            login(request=request, user=user)
            
            # creating user profile
            profile = UserProfile.objects.create(user=user)
            profile.save()

            return redirect("home")

        else:
            messages.error(request=request, message="Code didnt match!!!")
            return redirect("verify-email", username)