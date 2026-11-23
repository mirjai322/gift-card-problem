# Problem 00: Gift Cards

A tiny codebase (4 files) to warm up before Problem 01. Three short parts,
one per day, about 25–30 min each.

| Part | What you do | Skill it warms up |
|---|---|---|
| 1 | Fix a bug + validate input | Reading code, debugging a failing test, edge-case tests |
| 2 | History + expiration | Adding state, controlling time in tests |
| 3 | Tiny REST API | Status codes, JSON errors, testing endpoints |

## Setup (once)

```bash
cd p00_gift_cards
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -q        # expect 1 failing test: that's Part 1's bug
```

## Each session

1. Timer on. Read the code (2–3 min).
2. Say out loud: the task in one sentence, one example, what's unclear.
3. Code + run `pytest -q` often. Write your own tests.
4. No AI. Google/Python docs for syntax are fine.
5. When done: `git add -A && git commit -m "part N"`.

Next day: `python reveal.py 2` (then `3`).

To get reviewed, paste your diff into a chat: "review Problem 00 Part N".
