from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class CustomUserModel(AbstractUser):
    verification_code = models.IntegerField(default=000000)

    def __str__(self):
        return self.username

User = get_user_model()

class UserProfile(models.Model):

    relationship_choices = [
        ("none", "None"),
        ("single", "Single"),
        ("in_a_rel", "In a relationship"),
        ("merried", "Merried"),
        ("engaged", "Engaged"),
    ]

    followers = models.ManyToManyField(
        to=User,
        blank=True,
        related_name="followers_of"
    )
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=150, null=True, blank=True)
    pic = models.ImageField(upload_to="assets/images/avatars/", default="assets/images/avatars/avatar-1.jpg")
    locations = models.CharField(max_length=150, null=True, blank=True)
    working_at = models.CharField(max_length=55, null=True, blank=True)

    # choices

    relationship = models.CharField(max_length=50, choices=relationship_choices, default="none")

    # perms

    private = models.BooleanField(default=False)
    show_activity = models.BooleanField(default=True)
    allow_comms = models.BooleanField(default=True)


    # @property
    # def get_user(self):
    #     user = User.objects.get(id=self.user_id)
    #     return user

    def __str__(self):
        return self.user.username