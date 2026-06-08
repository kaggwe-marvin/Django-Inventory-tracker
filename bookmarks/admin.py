from typing import Any
from django.contrib import admin
from bookmarks.models import Bookmark, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ("title", "url", "created_at")
    list_filter = ("tags", "created_at")
    search_fields = ("title", "url", "description")
    ordering = ("-created_at",)
    filter_horizontal = ("tags",)  # Makes choosing multiple tags very clean in UI
