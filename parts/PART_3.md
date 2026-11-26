# Part 3: A tiny REST API  (~30 min)

> **Ticket**
>
> The checkout page needs to call us over HTTP. `app/api.py` already has
> `GET /gift_cards/<code>`. Add:
>
> | Method | Path | Body | Returns |
> |---|---|---|---|
> | POST | `/gift_cards` | `{"code": "...", "amount_cents": 2500}` | the new card |
> | POST | `/gift_cards/<code>/redemptions` | `{"amount_cents": 1000}` | the updated card |
> | GET  | `/gift_cards/<code>/history` | none | the history from Part 2 |
>
> 1. Pick the right **status codes**: created, success, bad input, not found,
>    and a duplicate code. Be ready to say why for each.
> 2. Bad input (missing field, a string instead of a number, malformed JSON)
>    returns a JSON error, **never a 500**.
> 3. **Tests** with Flask's test client:
>    ```python
>    client = create_app(GiftCardService()).test_client()
>    resp = client.post("/gift_cards", json={"code": "A", "amount_cents": 500})
>    assert resp.status_code == ...
>    ```

Then run it for real (`flask --app app.api run`) and try one request with curl.
