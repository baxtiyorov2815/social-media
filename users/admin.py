from django.contrib import admin

from .models import UserProfile, CustomUserModel

admin.site.register(UserProfile)
admin.site.register(CustomUserModel)