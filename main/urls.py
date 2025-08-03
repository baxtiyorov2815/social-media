from django.urls import path
from .views import HomePageView, PostUpload, DeletePostView, LikePostView, AddCommentView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path("upload-post/", PostUpload.as_view(), name="upload_post"),
    path("delete-post/<str:pk>/", DeletePostView.as_view(), name="delete_post"),
    path("like-post/<str:post_id>/", LikePostView.as_view(), name="like_post"),
    path("add-comment/<str:comment_id>/<uuid:post_id>/", AddCommentView.as_view(), name="add_comment")
]