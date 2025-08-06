from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from users.models import UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, LikePost, Comment, Notification
from django.contrib import messages
from PIL import Image
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import random

User = get_user_model()

def images_are_equal(img1, img2):
    return list(img1.getdata()) == list(img2.getdata())

class HomePageView(LoginRequiredMixin, View):
    login_url = "/auth/login/"
    template_name = 'index.html'
    def get(self, request):

        query = request.GET.get("q", "")
        results = []
        if query:
            users = User.objects.filter(username__icontains=query)[:10]
            for user in users:
                if user == request.user:
                    continue
                results.append({"id": user.id, "username": user.username})

            print(results)
            
            return JsonResponse({"results": results})

        liked_posts = []

        filter_user = LikePost.objects.filter(user=request.user)
        for like_post in filter_user:
            liked_posts.append(like_post.post.id)

        posts = Post.objects.all()[::-1]
        profiles = UserProfile.objects.all()
        user = request.user
        profile = UserProfile.objects.get(user=user)

        user_profiles = UserProfile.objects.all()
        user_suggestions = []
        for user_profile in user_profiles:
            if user not in user_profile.followers.all():
                user_suggestions.append(user_profile.user)
        if user in user_suggestions:
            user_suggestions.remove(user)


        now = timezone.now()

        for suggest in user_suggestions:
            suggest.days = (now-suggest.date_joined).days

        random.shuffle(user_suggestions)

        comments = Comment.objects.all()
        
        notifications = Notification.objects.filter(user=user).order_by("-created_at")
        unread_count = Notification.objects.filter(user=user, is_read=False).count()

        context = {
            'user': user,
            'profiles': profiles,
            'profile': profile,
            'posts': posts,
            'liked_posts': liked_posts,
            'user_suggestions': user_suggestions,
            'comments': comments,
            'unread_count': unread_count,
            'notifications': notifications[:5]
        }

        return render(request=request, template_name=self.template_name, context=context)
    
class NotificationView(LoginRequiredMixin, View):
    def get(self, reqeust, notification_id, *args, **kwargs):
        notification = get_object_or_404(Notification, id=notification_id, user=reqeust.user)

        notification.is_read = True
        notification.save()

        return JsonResponse(notification.get_target_data())

class UnreadNotificationCountView(LoginRequiredMixin, View):
    def get(self, request):
        count = request.user.received_notifications.filter(is_read=False).count()
        return JsonResponse({'count': count})


@method_decorator(csrf_exempt, name="dispatch")
class MarkAllNotificationsReadView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            updated = request.user.received_notifications.filter(is_read=False).update(is_read=True)

            return JsonResponse({
                'status': 'succes',
                'marked_read': updated
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

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

        profile = UserProfile.objects.get(user=user)
        followers = profile.followers.all()

        for follower in followers:
            Notification.objects.create(
                user=follower,
                sender=user,
                message=f"{user} posted a new photo",
                notification_type='post',
                content_id=str(post.id)
            )
        
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

            Notification.objects.create(
                user=post.user,
                sender=user,
                message=f"{user} liked your post",
                notification_type='like',
                content_id=str(post.id)
            )

        post.save()

        return JsonResponse({
            'liked': liked_status,
            'like_count': post.no_of_likes
        })
    

class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, comment_id, post_id, *args, **kwargs):
        
        parent = None
        text = request.POST.get('comment')
        
        if comment_id != 'None':
            parent = Comment.objects.get(id=int(comment_id))
            text = request.POST.get('text')
        
        author = request.user
        post = Post.objects.get(id=post_id)

        print(text)

        if parent != None:
            comment = Comment.objects.create(parent=parent, post=post, author=author, text=text)

            Notification.objects.create(
                user=parent.author,
                sender=author,
                message=f"{author.username} replied your comment",
                notification_type='reply',
                content_id=str(comment.id)
            )

        else:
            comment = Comment.objects.create(post=post, author=author, text=text)

            Notification.objects.create(
                user=post.user,
                sender=author,
                message=f"{author.username} commented on your post",
                notification_type="comment",
                content_id=str(comment.id)
            )

        comment.save()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'username': comment.author.username,
                'text': comment.text,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M')
            })

        return redirect('home')