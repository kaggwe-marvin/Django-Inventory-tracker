import logging
from typing import Any, Type
from django.db.models.signals import post_save
from django.dispatch import receiver
from inventory.models import Product

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Product)
def check_product_stock_threshold(
    sender: Type[Product], instance: Product, created: bool, **kwargs: Any
) -> None:
    """Listens for product changes and flags low stock instantly."""
    # Check if the product instance falls below the tracking threshold
    if instance.stock <= instance.low_stock_threshold:
        # For this stage, we will print to console and log out an alert string
        print(
            f"\n[ALERT] LOW STOCK WARNING: '{instance.name}' has only {instance.stock} left!"
        )
        logger.warning("SKU %s threshold reached.", instance.sku)
