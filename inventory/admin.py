from typing import Any
from django.contrib import admin
from django.utils.html import format_html
from inventory.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = (
        "name",
        "sku",
        "stock",
        "low_stock_threshold",
        "stock_status_flag",
    )
    list_filter = ("updated_at",)
    search_fields = ("name", "sku")
    readonly_fields = ("updated_at",)

    @admin.display(description="Status")
    def stock_status_flag(self, obj: Product) -> Any:
        """Renders a visual indicator label directly inside the grid row."""
        if obj.stock <= obj.low_stock_threshold:
            return format_html(
                '<span style="color: red; font-weight: bold;">⚠️ LOW STOCK</span>'
            )
        return format_html(
            '<span style="color: green; font-weight: bold;">✅ HEALTHY</span>'
        )
