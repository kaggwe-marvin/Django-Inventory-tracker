from django.urls import path
from api.views import CachedBookmarkListAPIView

app_name = "api"

urlpatterns = [
    path("v1/bookmarks/", CachedBookmarkListAPIView.as_view(), name="bookmark-list"),
]
