from django.urls import path
from .views import HomePageView, PostUpload, DeletePostView, LikePostView, AddCommentView, NotificationView, UnreadNotificationCountView, MarkAllNotificationsReadView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path("upload-post/", PostUpload.as_view(), name="upload_post"),
    path("delete-post/<str:pk>/", DeletePostView.as_view(), name="delete_post"),
    path("like-post/<str:post_id>/", LikePostView.as_view(), name="like_post"),
    path("add-comment/<str:comment_id>/<uuid:post_id>/", AddCommentView.as_view(), name="add_comment"),
    path("notification/<int:notification_id>/", NotificationView.as_view(), name="notification_view"),
    path('notifications/unread_count/', UnreadNotificationCountView.as_view(), name='unread_count'),
    path('notifications/mark_all_read/', MarkAllNotificationsReadView.as_view(), name='mark_all_read')
]