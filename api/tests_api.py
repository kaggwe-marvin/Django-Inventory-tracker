import pytest
from django.core.cache import cache
from django.urls import reverse
from rest_framework.test import APIClient
from bookmarks.models import Bookmark


@pytest.fixture(autouse=True)
def clear_cache_each_run() -> None:
    """Ensures each test execution isolation loop runs with an empty cache."""
    cache.clear()


@pytest.mark.django_db
def test_api_view_caches_database_responses() -> None:
    client = APIClient()
    url = reverse("api:bookmark-list")

    # 1. Setup sample record data
    Bookmark.objects.create(title="Cache Target", url="https://cacheme.com")

    # 2. First hit: Executes database query and populates cache storage
    response_one = client.get(url)
    assert response_one.status_code == 200
    assert len(response_one.json()) == 1

    # 3. Add a second record directly to the database behind the scenes
    Bookmark.objects.create(title="Ghost Record", url="https://ghost.com")

    # 4. Second hit: Should serve from cache, meaning the new item isn't returned yet
    response_two = client.get(url)
    assert response_two.status_code == 200
    assert len(response_two.json()) == 1  # Still 1 due to active cache hit!

    # 5. Clear the cache completely
    cache.clear()

    # 6. Third hit: Cache miss forces database sync, picking up the new record
    response_three = client.get(url)
    assert len(response_three.json()) == 2


@pytest.mark.django_db
def test_throttle_middleware_blocks_abuse() -> None:
    client = APIClient()
    url = reverse("api:bookmark-list")

    # Fire 60 successive successful requests safely under the limit threshold
    for _ in range(60):
        response = client.get(url)
        assert response.status_code == 200

    # The 61st request must trigger the throttle boundary condition
    abusive_response = client.get(url)
    assert abusive_response.status_code == 429
    assert (
        abusive_response.json()["error"]
        == "API rate limit exceeded. Retry in a minute."
    )
