import pytest

from app.errors import NotFoundError, ValidationError
from app.gift_card_service import GiftCardService

from datetime import datetime, timedelta, timezone



@pytest.fixture
def service():
    s = GiftCardService()
    s.issue("WELCOME25", 2_500)
    return s


def test_issue_and_get(service):
    assert service.get("WELCOME25").balance_cents == 2_500

def test_cannot_overdraw(service):
    with pytest.raises(ValidationError):
        service.redeem("WELCOME25", 3_000)
    assert service.get("WELCOME25").balance_cents == 2_500

def test_cannot_redeem_0(service):
    with pytest.raises(ValidationError):
        service.redeem("WELCOME25", 0)

def test_duplicate_code_rejected(service):
    with pytest.raises(ValidationError):
        service.issue("WELCOME25", 1_000)


def test_unknown_code(service):
    with pytest.raises(NotFoundError):
        service.get("NOPE")


def test_partial_redeem(service):
    card = service.redeem("WELCOME25", 1_000)
    assert card.balance_cents == 1_500


def test_cannot_redeem_more_than_balance(service):
    with pytest.raises(ValidationError):
        service.redeem("WELCOME25", 3_000)
    assert service.get("WELCOME25").balance_cents == 2_500

def test_expired_card_cannot_be_redeemed():
    service = GiftCardService()
    past = datetime.now(timezone.utc) - timedelta(hours=1)
    service.issue("OLD", 1000, expires_at=past)
    with pytest.raises(ValidationError):
        service.redeem("OLD", 100)