from django.urls import path
from .views import HomePageView, PostUpload, DeletePostView, LikePostView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path("upload-post/", PostUpload.as_view(), name="upload_post"),
    path("delete-post/<str:pk>/", DeletePostView.as_view(), name="delete_post"),
    path("like-post/<str:post_id>/", LikePostView.as_view(), name="like_post"),
]