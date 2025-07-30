from django.urls import path
from .views import HomePageView, PostUpload

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path("upload-post/", PostUpload.as_view(), name="upload_post")
]