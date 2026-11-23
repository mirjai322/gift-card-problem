"""Run locally:  flask --app app.api run --port 5000"""
from flask import Flask, jsonify

from app.errors import NotFoundError
from app.gift_card_service import GiftCardService


def create_app(service=None) -> Flask:
    app = Flask(__name__)
    service = service or GiftCardService()

    @app.errorhandler(NotFoundError)
    def not_found(err):
        return jsonify(error=str(err)), 404

    @app.get("/gift_cards/<code>")
    def get_gift_card(code):
        card = service.get(code)
        return jsonify(code=card.code, balance_cents=card.balance_cents), 200

    return app


app = create_app()
