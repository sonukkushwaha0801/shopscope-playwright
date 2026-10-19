"""Small provider-based service for future price tracking."""

from dataclasses import dataclass
from decimal import Decimal

from shopscope.adapters.base import OfferProvider, ProductOffer


@dataclass(frozen=True, slots=True)
class PriceChange:
    previous: Decimal
    current: Decimal

    @property
    def amount(self) -> Decimal:
        return self.current - self.previous

    @property
    def decreased(self) -> bool:
        return self.current < self.previous


class PriceTrackingService:
    """Business logic separated from provider access and browser automation."""

    def __init__(self, provider: OfferProvider) -> None:
        self._provider = provider

    def fetch_offer(self, product_id: str) -> ProductOffer:
        """Fetch an offer from an explicitly configured provider."""
        return self._provider.get_offer(product_id)

    @staticmethod
    def compare(previous: Decimal, current: Decimal) -> PriceChange:
        """Compare two prices without floating-point arithmetic."""
        if previous < 0 or current < 0:
            raise ValueError("Prices cannot be negative.")
        return PriceChange(previous=previous, current=current)
