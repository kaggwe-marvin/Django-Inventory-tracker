import pytest
from inventory.models import Product


@pytest.mark.django_db
def test_signal_triggers_low_stock_alert(capsys: pytest.CaptureFixture[str]) -> None:
    # 1. Setup - Create a product with healthy stock levels
    product = Product.objects.create(
        name="Wireless Mouse", sku="MS-100", stock=10, low_stock_threshold=3
    )

    # 2. Action - Drop stock below threshold and save
    product.stock = 2
    product.save()

    # 3. Assert - Check console output using pytest capsys fixture
    captured = capsys.readouterr()
    assert "[ALERT] LOW STOCK WARNING" in captured.out
    assert "Wireless Mouse" in captured.out
