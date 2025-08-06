from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import UserProfile
from main.models import Comment, Notification
from django.contrib import messages
from django.contrib.auth import get_user_model
from main.models import Post
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()

# Create your views here.
class ProfileSettingsView(LoginRequiredMixin, View):
    login_url = "/auth/login/"
    template_name = "users/setting.html"
    
    def get(self, request):
        user = request.user
        profile = UserProfile.objects.get(user=user)
        followers_count = profile.followers.all().count()
        following_count = User.objects.filter(userprofile__followers=user).count()
        return render(request=request,
                      template_name=self.template_name,
                      context={"user": user, "profile": profile, "followers_count": followers_count, "following_count": following_count})
    
    def post(self, request, *args, **kwargs):
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        bio = request.POST.get("bio")
        location = request.POST.get("location")
        working_at = request.POST.get("working_at")
        relationship = request.POST.get("relationship")
        private = request.POST.get("private")
        show_activity = request.POST.get("show_activity")
        allow_comms = request.POST.get("allow_comms")
        pic = request.FILES.get("avatar")

        user = request.user
        profile = UserProfile.objects.get(user=user)

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        profile.bio = bio
        profile.locations = location
        profile.working_at = working_at
        profile.relationship = relationship

        profile.private = bool(private)
        profile.show_activity = bool(show_activity)
        profile.allow_comms = bool(allow_comms)
        if pic:
            profile.pic=pic

        profile.save()
        messages.info(request=request, message=f"Account: {user.username} changed succesfully!!!")
        return redirect("home")

class ProfilePageView(LoginRequiredMixin, View):
    login_url = "/auth/login/"
    template_name = "users/profile.html"

    def get(self, request, username, *args, **kwargs):
        user = User.objects.get(username=username)
        profile = UserProfile.objects.get(user=user)
        posts = Post.objects.filter(user=user)
        comments = Comment.objects.all()
        followers_count = profile.followers.all().count()
        following_count = User.objects.filter(userprofile__followers=user).count()
        return render(request=request, template_name=self.template_name, context={"user": user, "posts": posts, "profile": profile, "followers_count": followers_count, "following_count": following_count, "comments": comments})
    
    def post(self, request, username, *args, **kwargs):
        current_user = request.user
        target_user = User.objects.get(username=username)
        
        if current_user == target_user:
            return redirect('profile', username)
        
        target_profile = get_object_or_404(UserProfile, user=target_user)
        current_profile = get_object_or_404(UserProfile, user=current_user)

        if current_user not in target_profile.followers.all():
            target_profile.followers.add(current_user)
        else:
            target_profile.followers.remove(current_user)
        
        return redirect("profile", username)

class FollowersPageView(LoginRequiredMixin, View):

    login_url = "/auth/login/"
    template_name = "users/followers.html"

    def get(self, request, username, *args, **kwargs):
        user = User.objects.get(username=username)
        profile = UserProfile.objects.get(user=user)
        followers = profile.followers.all()
        followers_count = followers.count()
        following_count = User.objects.filter(userprofile__followers=user).count()
        return render(request=request, template_name=self.template_name, context={"followers": followers, "followers_count": followers_count, "following_count": following_count, "user": user})

    def post(self, request, username, *args, **kwargs):
        current_user = request.user
        current_user_profile = UserProfile.objects.get(user=current_user)
        user_to_remove = User.objects.get(username=username)
        current_user_profile.followers.remove(user_to_remove)

        return redirect("followers", current_user.username)

class FollowingView(LoginRequiredMixin, View):
    def get(self, request, username, *args, **kwargs):
        user = User.objects.get(username=username)
        profile = UserProfile.objects.get(user=user)

        following_users = User.objects.filter(userprofile__followers=user)

        context = {
            "following_users": following_users,
            "followers_count": profile.followers.count(),
            "following_count": User.objects.filter(userprofile__followers=user).count(),
            "user": user,
        }

        return render(request, "users/following.html", context)

    def post(self, request, username, *args, **kwargs):
        current_user = request.user
        user2 = User.objects.get(username=username)
        user2_profile = UserProfile.objects.get(user=user2)
        user2_profile.followers.remove(current_user)
        return redirect("following", request.user.username)
    

class FollowUser(LoginRequiredMixin, View):
    def post(self, request, username, *args, **kwargs):
        current_user = request.user
        try:
            user_to_follow = User.objects.get(username=username)
            user_to_follow_profile = UserProfile.objects.get(user=user_to_follow)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        if current_user in user_to_follow_profile.followers.all():
            user_to_follow_profile.followers.remove(current_user)
            following = False
        else:
            user_to_follow_profile.followers.add(current_user)
            following = True
            Notification.objects.create(
                user=user_to_follow,
                sender=current_user,
                message=f"{current_user.username} followed you",
                notification_type="follow",
                content_id=str(current_user.id)
            )

        return JsonResponse({
            "following": following,
            "follower_count": user_to_follow_profile.followers.count()
        })