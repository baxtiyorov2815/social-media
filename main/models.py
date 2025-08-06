import uuid
from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="assets/images/post/")
    desc = models.TextField(default="hello world")
    created_at = models.DateTimeField(default=datetime.now())
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
    
class LikePost(models.Model):
    post = models.ForeignKey(to=Post,
                             on_delete=models.CASCADE,
                             )
    user = models.ForeignKey(to=User,
                             on_delete=models.CASCADE,
                             )
    
    def __str__(self):
        return self.user.username
    
class Comment(models.Model):
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies")
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username} - {self.text[:30]}'
    
    def is_reply(self):
        return self.parent is not None
    
class Notification(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='received_notifications')
    message = models.CharField(max_length=250)
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=50) # comment, post, reply, follow
    content_id = models.CharField(max_length=36) # ID of user/ post/ comment/ like && Charfield becouse post model's id is uuid4
    sender = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='sent_notifications')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_target_data(self):
        data = {
            'type': self.notification_type,
            'content_id': self.content_id,
            'message': self.message,
            'sender_username': self.sender.username  # Always include sender username
        }
        
        # Add type-specific data
        if self.notification_type == 'follow':
            data['profile_username'] = self.sender.username
        elif self.notification_type == 'post':
            data['post_id'] = self.content_id  # This is the UUID of the post
        elif self.notification_type == 'like':
            data['post_id'] = self.content_id  # The post that was liked
        elif self.notification_type == 'comment':
            data['post_id'] = Post.objects.get(comments__id=self.content_id).id  # Get post ID from comment
            data['comment_id'] = self.content_id
        elif self.notification_type == 'reply':
            comment = Comment.objects.get(id=self.content_id)
            data['post_id'] = comment.post.id
            data['comment_id'] = self.content_id
            data['parent_comment_id'] = comment.parent.id if comment.parent else None
        
        return data
    
    def __str__(self):
        return self.user + self.message[:20]