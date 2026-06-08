import pytest
from bookmarks.forms import BookmarkForm
from bookmarks.models import Bookmark, Tag


@pytest.mark.django_db
def test_bookmark_form_creates_tags_automatically() -> None:
    # 1. Setup form payload containing raw string tags
    form_data = {
        "title": "Django Project",
        "url": "https://djangoproject.com",
        "description": "The web framework for perfectionists.",
        "tags_input": "python, web, open-source",
    }

    # 2. Run form validation and save operations
    form = BookmarkForm(data=form_data)
    assert form.is_valid()
    bookmark = form.save()

    # 3. Assert relationship structures persist perfectly
    assert bookmark.tags.count() == 3
    assert Tag.objects.filter(slug="open-source").exists()
    assert bookmark.tags.filter(name="python").exists()
