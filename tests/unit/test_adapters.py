"""Unit tests for normalized provider models."""

from decimal import Decimal

from shopscope.adapters.base import ProductOffer


def test_product_offer_uses_decimal_price():
    offer = ProductOffer(
        retailer="approved-provider",
        product_id="SKU-001",
        title="Example item",
        price=Decimal("199.99"),
        currency="INR",
        product_url="https://example.invalid/products/SKU-001",
    )

    assert offer.price == Decimal("199.99")
    assert offer.currency == "INR"
