from typing import Any
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from bookmarks.forms import BookmarkForm
from bookmarks.models import Bookmark


# We use a type comment to tell mypy this is a ListView handling Bookmarks
class BookmarkListView(ListView):  # type: ignore[type-arg]
    model = Bookmark
    template_name = "bookmarks/bookmark_list.html"
    context_object_name = "bookmarks"

    def get_queryset(self) -> Any:
        return Bookmark.objects.prefetch_related("tags")


# We use a type comment to tell mypy this is a CreateView handling Bookmarks
class BookmarkCreateView(CreateView):  # type: ignore[type-arg]
    model = Bookmark
    form_class = BookmarkForm
    template_name = "bookmarks/bookmark_form.html"
    success_url = reverse_lazy("bookmarks:list")
