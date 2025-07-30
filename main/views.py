from django.shortcuts import render
from django.views import View
from users.models import UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post

class HomePageView(LoginRequiredMixin, View):
    login_url = "/auth/login/"
    template_name = 'index.html'
    def get(self, request):
        
        posts = Post.objects.all()
        profiles = UserProfile.objects.all()
        user = request.user
        profile = UserProfile.objects.get(user=user)

        # Mapping: user.id → profile
        profile_map = { profile.user_id: profile for profile in profiles }

        context = {
            'user': user,
            'profiles': profiles,
            'profile': profile,
            'posts': posts,
            'profile_map': profile_map
        }

        return render(request=request, template_name=self.template_name, context=context)
    
class PostUpload(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pass
    def post(self, request, *args, **kwargs):
        image = request.FILES.get('image')
        print(image)