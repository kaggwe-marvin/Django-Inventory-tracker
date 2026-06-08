from typing import Any
from django.db import models


class ProductQuerySet(models.QuerySet):  # type: ignore[type-arg]
    def low_stock(self) -> "ProductQuerySet":
        """Filter products where stock falls below the threshold."""
        return self.filter(stock__lte=models.F("low_stock_threshold"))


# Pass the QuerySet into the manager to make the method chainable
ProductManager = models.Manager.from_queryset(ProductQuerySet)


class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=50, unique=True)
    stock = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=5)
    updated_at = models.DateTimeField(auto_now=True)

    # Attach our type-hinted custom manager engine
    objects = ProductManager()

    def __str__(self) -> str:
        return f"{self.name} (SKU: {self.sku})"
