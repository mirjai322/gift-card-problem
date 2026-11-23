from typing import Dict

from app.errors import NotFoundError, ValidationError
from app.models import GiftCard


class GiftCardService:
    """Issues gift cards and keeps track of their balances (in cents)."""

    def __init__(self) -> None:
        self._cards: Dict[str, GiftCard] = {}

    def issue(self, code: str, amount_cents: int) -> GiftCard:
        if amount_cents <= 0:
            raise ValidationError("amount must be positive")
        if code in self._cards:
            raise ValidationError(f"code '{code}' already exists")
        card = GiftCard(code=code, balance_cents=amount_cents)
        self._cards[code] = card
        return card

    def get(self, code: str) -> GiftCard:
        card = self._cards.get(code)
        if card is None:
            raise NotFoundError(f"gift card '{code}' not found")
        return card

    def redeem(self, code: str, amount_cents: int) -> GiftCard:
        """Spend amount_cents from the card. Returns the updated card."""
        card = self.get(code)
        card.balance_cents -= amount_cents
        return card
