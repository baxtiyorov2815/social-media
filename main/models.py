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