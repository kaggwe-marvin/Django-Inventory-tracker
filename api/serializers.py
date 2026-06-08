from rest_framework import serializers
from bookmarks.models import Bookmark


class BookmarkSerializer(serializers.ModelSerializer):  # type: ignore[misc]
    # Explicitly pull in read-only nested representation of our tags
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")

    class Meta:
        model = Bookmark
        fields = ["id", "title", "url", "description", "tags", "created_at"]
