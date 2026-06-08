from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from inventory.models import Product


class Command(BaseCommand):
    help = "Simulates daily sales by depleting stock values for all inventory items."

    def add_arguments(self, parser: CommandParser) -> None:
        # Accept an argument to define depletion rate
        parser.add_argument(
            "--amount",
            type=int,
            default=1,
            help="The integer amount of units to subtract from every product's stock.",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        amount: int = options["amount"]
        products = Product.objects.all()
        updated_count = 0

        for product in products:
            # Prevent negative stock numbers
            if product.stock >= amount:
                product.stock -= amount
            else:
                product.stock = 0

            # This save action will iteratively fire our low-stock warning signal!
            product.save()
            updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully processed sales simulation across {updated_count} products."
            )
        )
