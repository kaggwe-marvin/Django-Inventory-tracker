from django import forms
from django.utils.text import slugify
from bookmarks.models import Bookmark, Tag


class BookmarkForm(forms.ModelForm):  # type: ignore[type-arg]
    # Virtual field to accept comma-separated tags
    tags_input = forms.CharField(
        label="Tags",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "e.g., python, django, backend"}),
    )

    class Meta:
        model = Bookmark
        fields = ["title", "url", "description"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "e.g., Django Docs"}),
            "url": forms.URLInput(attrs={"placeholder": "https://..."}),
            "description": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Optional summary..."}
            ),
        }

    def save(self, commit: bool = True) -> Bookmark:
        # Save the Bookmark instance first
        bookmark = super().save(commit=False)
        if commit:
            bookmark.save()

        # Process the tag string split by commas
        tag_data = self.cleaned_data.get("tags_input", "")
        if tag_data:
            tag_names = [t.strip() for t in tag_data.split(",") if t.strip()]

            # Clear existing tags if updating
            if bookmark.pk and commit:
                bookmark.tags.clear()

            for name in tag_names:
                # Find or create each tag dynamically
                tag, _ = Tag.objects.get_or_create(
                    name=name, defaults={"slug": slugify(name)}
                )
                bookmark.tags.add(tag)

        return bookmark  # type: ignore[no-any-return]
