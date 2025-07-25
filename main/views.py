from django.shortcuts import render
from django.views import View
from users.models import UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin

class HomePageView(LoginRequiredMixin, View):
    login_url = "/auth/login/"
    def get(self, request):
        template_name = 'index.html'
        user = request.user
        profile = UserProfile.objects.get(user=user)
        print("image: ", profile.pic.url)
        return render(request=request, template_name=template_name, context={"user": user, "profile": profile})