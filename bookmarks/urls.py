from django.urls import path
from bookmarks.views import BookmarkCreateView, BookmarkListView

app_name = "bookmarks"

urlpatterns = [
    path("", BookmarkListView.as_view(), name="list"),
    path("add/", BookmarkCreateView.as_view(), name="create"),
]
