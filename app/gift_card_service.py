from typing import Dict, Optional

from app.errors import NotFoundError, ValidationError
from app.models import GiftCard, EventType
from datetime import datetime, timezone



class GiftCardService:
    """Issues gift cards and keeps track of their balances (in cents)."""

    def __init__(self) -> None:
        self._cards: Dict[str, GiftCard] = {}

    def issue(self, code: str, amount_cents: int, expires_at: Optional[datetime] = None) -> GiftCard:
        if amount_cents <= 0:
            raise ValidationError("amount must be positive")
        if code in self._cards:
            raise ValidationError(f"code '{code}' already exists")
        card = GiftCard(code=code, balance_cents=amount_cents, expires_at=expires_at)
        self._cards[code] = card
        card.history.append((EventType.ISSUED, amount_cents, card.balance_cents, datetime.now(timezone.utc)))
        return card

    def get(self, code: str) -> GiftCard:
        card = self._cards.get(code)
        if card is None:
            raise NotFoundError(f"gift card '{code}' not found")
        return card

    def redeem(self, code: str, amount_cents: int) -> GiftCard:
        """Spend amount_cents from the card. Returns the updated card."""
        card = self.get(code)
        if amount_cents > card.balance_cents:
            raise ValidationError("not enough balance")
        if amount_cents <= 0:
            raise ValidationError("amount must be positive")
        if card.expires_at is not None and datetime.now(timezone.utc) >= card.expires_at:
            raise ValidationError("card is expired")
        card.balance_cents -= amount_cents
        card.history.append((EventType.REDEEMED, amount_cents, card.balance_cents, datetime.now(timezone.utc)))
        return card
