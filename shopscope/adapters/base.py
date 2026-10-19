"""Provider contracts for future retailer or price-data integrations."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol


@dataclass(frozen=True, slots=True)
class ProductOffer:
    """Normalized offer model independent of a retailer's page structure."""

    retailer: str
    product_id: str
    title: str
    price: Decimal
    currency: str
    product_url: str


class OfferProvider(Protocol):
    """Interface implemented by an approved API or licensed data provider."""

    def get_offer(self, product_id: str) -> ProductOffer:
        """Return one normalized offer or raise a provider-specific exception."""
        ...
