from dataclasses import dataclass


@dataclass
class GiftCard:
    code: str
    balance_cents: int
