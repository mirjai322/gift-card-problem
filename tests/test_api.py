import pytest

from app.api import create_app
from app.gift_card_service import GiftCardService


@pytest.fixture
def client():
    """A fake HTTP client. Sends requests to the app without starting a server."""
    return create_app(GiftCardService()).test_client()


@pytest.fixture
def client_with_card(client):
    client.post("/gift_cards", json={"code": "WELCOME25", "amount_cents": 2_500})
    return client


# --- Issuing ---

def test_issue_returns_201_and_card(client):
    resp = client.post("/gift_cards", json={"code": "A", "amount_cents": 500})
    assert resp.status_code == 201
    assert resp.get_json() == {"code": "A", "balance_cents": 500}


def test_duplicate_code_is_rejected(client_with_card):
    resp = client_with_card.post("/gift_cards", json={"code": "WELCOME25", "amount_cents": 100})
    assert resp.status_code == 400   # change to 409 if you add ConflictError
    assert "error" in resp.get_json()


def test_missing_field_is_400(client):
    resp = client.post("/gift_cards", json={"code": "A"})
    assert resp.status_code == 400
    assert "amount_cents" in resp.get_json()["error"]


def test_amount_as_string_is_400(client):
    resp = client.post("/gift_cards", json={"code": "A", "amount_cents": "500"})
    assert resp.status_code == 400


def test_malformed_json_is_400(client):
    resp = client.post("/gift_cards", data="not json", content_type="application/json")
    assert resp.status_code == 400


# --- Getting ---

def test_get_card(client_with_card):
    resp = client_with_card.get("/gift_cards/WELCOME25")
    assert resp.status_code == 200
    assert resp.get_json()["balance_cents"] == 2_500


def test_get_unknown_card_is_404(client):
    assert client.get("/gift_cards/NOPE").status_code == 404


# --- Redeeming ---

def test_redeem_updates_balance(client_with_card):
    resp = client_with_card.post("/gift_cards/WELCOME25/redemptions", json={"amount_cents": 1_000})
    assert resp.status_code == 200
    assert resp.get_json()["balance_cents"] == 1_500


def test_redeem_more_than_balance_is_400_and_balance_unchanged(client_with_card):
    resp = client_with_card.post("/gift_cards/WELCOME25/redemptions", json={"amount_cents": 9_999})
    assert resp.status_code == 400
    assert client_with_card.get("/gift_cards/WELCOME25").get_json()["balance_cents"] == 2_500


def test_redeem_unknown_card_is_404(client):
    resp = client.post("/gift_cards/NOPE/redemptions", json={"amount_cents": 100})
    assert resp.status_code == 404


# --- History ---

def test_history_after_issue_and_redeem(client_with_card):
    client_with_card.post("/gift_cards/WELCOME25/redemptions", json={"amount_cents": 1_000})
    resp = client_with_card.get("/gift_cards/WELCOME25/history")
    assert resp.status_code == 200
    events = resp.get_json()["data"]
    assert [e["type"] for e in events] == ["issued", "redeemed"]
    assert events[-1]["balance_after_cents"] == 1_500