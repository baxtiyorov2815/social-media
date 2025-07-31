from django.shortcuts import render, redirect
from django.views import View
from users.models import UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from django.contrib import messages

class HomePageView(LoginRequiredMixin, View):
    login_url = "/auth/login/"
    template_name = 'index.html'
    def get(self, request):
        
        posts = Post.objects.all()[::-1]
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
        desc = request.POST.get("caption")
        is_exist = Post.objects.filter(image=image, desc=desc).exists()
        if is_exist:
            user = Post.objects.get(image=image, desc=desc).user

            messages.warning(request=request, message=f"This post already exists !!! posted by {user.username}")
        else:
            user = request.user
            post = Post.objects.create(user=user, image=image, desc=desc)
            post.save()

            messages.success(request=request, message="Post has been created succesfully")

        return redirect('home')
            