from django.apps import AppConfig


class InventoryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "inventory"

    def ready(self) -> None:
        # Import signals to ensure they attach to their database senders
        import inventory.signals  # noqa
