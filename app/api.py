"""Run locally:  flask --app app.api run --port 5000"""
from flask import Flask, jsonify, request

from app.errors import NotFoundError, ValidationError
from app.gift_card_service import GiftCardService

def card_to_dict(card):
    return {"code": card.code, "balance_cents": card.balance_cents}


def require_json_fields(*fields):
    """Read the JSON body and make sure the listed fields are present."""
    body = request.get_json(silent=True)   # None instead of crashing on bad JSON
    if not isinstance(body, dict):
        raise ValidationError("request body must be a JSON object")
    missing = [f for f in fields if f not in body]
    if missing:
        raise ValidationError(f"missing field(s): {', '.join(missing)}")
    return body


def require_int(body, field):
    value = body[field]
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValidationError(f"{field} must be an integer")
    return value


def create_app(service=None) -> Flask:
    app = Flask(__name__)
    service = service or GiftCardService()

    @app.errorhandler(NotFoundError)
    def not_found(err):
        return jsonify(error=str(err)), 404

    @app.errorhandler(ValidationError)
    def bad_request(err):
        return jsonify(error=str(err)), 400

    @app.get("/gift_cards/<code>")
    def get_gift_card(code):
        card = service.get(code)
        return jsonify(code=card.code, balance_cents=card.balance_cents), 200

    @app.post("/gift_cards")
    def issue_gift_card():
        body = require_json_fields("code", "amount_cents")
        card = service.issue(body["code"], require_int(body, "amount_cents"))
        return jsonify(code=card.code, balance_cents=card.balance_cents), 201

    @app.post("/gift_cards/<code>/redemptions")
    def redeem_gift_card(code):
        body = require_json_fields("amount_cents")
        card = service.redeem(code, require_int(body, "amount_cents"))
        return jsonify(card_to_dict(card)), 200

    @app.get("/gift_cards/<code>/history")
    def get_history(code):
        card = service.get(code)
        events = [
            {
                "type": event_type.value,
                "amount_cents": amount,
                "balance_after_cents": balance_after,
                "at": at.isoformat(),
            }
            for (event_type, amount, balance_after, at) in card.history
        ]
        return jsonify(data=events), 200

    return app


app = create_app()
