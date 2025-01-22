from django.urls import path
from .views import (
    UploadMediaView,
    MediaLibraryView,
    CreatePostView,
    ListPostsView,
    ModeratePostView,
    SchedulePostView,
    ListScheduledPostsView,
    BulkScheduleView,
)

app_name = "content_management"

urlpatterns = [
    path("media/upload/", UploadMediaView.as_view(), name="upload_media"),
    path("media/", MediaLibraryView.as_view(), name="list_media"),
    path("posts/create/", CreatePostView.as_view(), name="create_post"),
    path("posts/", ListPostsView.as_view(), name="list_posts"),
    path("posts/<int:pk>/", ModeratePostView.as_view(), name="moderate_post"),
    path("schedule/", SchedulePostView.as_view(), name="schedule_post"),
    path("schedule/calendar/", ListScheduledPostsView.as_view(), name="list_scheduled_posts"),
    path("schedule/bulk/", BulkScheduleView.as_view(), name="bulk_schedule"),
]
