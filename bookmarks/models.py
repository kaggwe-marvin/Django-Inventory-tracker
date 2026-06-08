from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self) -> str:
        return str(self.name)


class Bookmark(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=500, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = models.ManyToManyField(Tag, related_name="bookmarks")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return str(self.title)
