from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from users.models import UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, LikePost
from django.contrib import messages
from PIL import Image
from io import BytesIO
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect

def images_are_equal(img1, img2):
    return list(img1.getdata()) == list(img2.getdata())

class HomePageView(LoginRequiredMixin, View):
    login_url = "/auth/login/"
    template_name = 'index.html'
    def get(self, request):

        liked_posts = []

        filter_user = LikePost.objects.filter(user=request.user)
        for like_post in filter_user:
            liked_posts.append(like_post.post.id)

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
            'profile_map': profile_map,
            'liked_posts': liked_posts
        }

        return render(request=request, template_name=self.template_name, context=context)
    
class PostUpload(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        image = request.FILES.get('image')
        desc = request.POST.get("caption")

        uploaded_img = Image.open(image)

        for post in Post.objects.filter(desc=desc):
            try:
                with post.image.open('rb') as f:
                    existing_img = Image.open(f)
                    if images_are_equal(uploaded_img, existing_img):
                        messages.warning(request=request, message=f"This post already exists !!! posted by {post.user.username}")
                        return redirect("home")
            except:
                continue
        
        user = request.user
        post = Post.objects.create(user=user, image=image, desc=desc)
        post.save()
        
        messages.success(request=request, message="Post has been created succesfully")

        return redirect('home')
    

class DeletePostView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)

        if post.user != request.user:
            messages.error(request, "You don't have permission to delete this post.")
            return redirect('home')

        post.delete()
        messages.warning(request, "Post has been deleted successfully!")
        return redirect('home')
    
class LikePostView(LoginRequiredMixin, View):
    def post(self, request, post_id, *args, **kwargs):
        post = Post.objects.get(id=post_id)
        user = request.user

        liked = LikePost.objects.filter(post=post, user=user).first()

        if liked:
            liked.delete()
            post.no_of_likes -= 1
            liked_status = False
        
        else:
            LikePost.objects.create(post=post, user=user)
            post.no_of_likes += 1
            liked_status = True

        post.save()

        return JsonResponse({
            'liked': liked_status,
            'like_count': post.no_of_likes
        })