from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

# Create your views here.
class ProfileSettingsView(LoginRequiredMixin, View):
    login_url = "/auth/login/"
    template_name = "users/setting.html"
    
    def get(self, request):
        return render(request=request,
                      template_name=self.template_name)
    
    def post(self, request, *args, **kwargs):
        pass

class ProfilePageView(LoginRequiredMixin, View):
    login_url = "/auth/login/"
    template_name = "users/profile.html"
    
    def get(self, request, *args, **kwargs):
        user = request.user

        return render(request=request, template_name=self.template_name, context={"user": user})
    
    def post(self, request, *args, **kwargs):
        pass