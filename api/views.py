from typing import Any
from django.conf import settings
from rest_framework.request import Request
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import ListAPIView
from bookmarks.models import Bookmark
from api.serializers import BookmarkSerializer


class CachedBookmarkListAPIView(ListAPIView):  # type: ignore[misc]
    queryset = Bookmark.objects.prefetch_related("tags")
    serializer_class = BookmarkSerializer

    def check_permissions(self, request: Request) -> None:
        """Enforces a strict, lightweight authorization header check."""
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        expected_token = f"Bearer {getattr(settings, 'API_SECRET_TOKEN', 'dev-secret')}"

        if not auth_header or auth_header != expected_token:
            raise AuthenticationFailed("Invalid or missing developer API token.")

        super().check_permissions(request)
