from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from datetime import datetime

class EventType(str, Enum):
    ISSUED = "issued"
    REDEEMED = "redeemed"

@dataclass
class GiftCard:
    code: str
    balance_cents: int
    history: list = field(default_factory=list)
    expires_at: Optional[datetime] = None
