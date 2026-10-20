from decimal import Decimal

import pytest

from shopscope.tracking.service import PriceTrackingService


def test_price_decrease_is_detected() -> None:
    change = PriceTrackingService.compare(Decimal("100.00"), Decimal("79.50"))
    assert change.decreased is True
    assert change.amount == Decimal("-20.50")


def test_price_increase_is_not_a_decrease() -> None:
    change = PriceTrackingService.compare(Decimal("50"), Decimal("65"))
    assert change.decreased is False
    assert change.amount == Decimal("15")


@pytest.mark.parametrize("price", [Decimal("-0.01"), Decimal("-10")])
def test_negative_prices_are_rejected(price: Decimal) -> None:
    with pytest.raises(ValueError, match="cannot be negative"):
        PriceTrackingService.compare(price, Decimal("1"))
