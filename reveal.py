"""Unseal the next part:  python reveal.py 2

Parts are base64-encoded so you can't spoil them by accident. Only reveal
the next part once the current one is done (or you've hit your timer).
"""
import base64
import sys
from pathlib import Path

PARTS = Path(__file__).parent / "parts"

if len(sys.argv) != 2 or not sys.argv[1].isdigit():
    sys.exit("usage: python reveal.py <part number>")

n = sys.argv[1]
sealed = PARTS / f"part_{n}.sealed"
if not sealed.exists():
    sys.exit(f"no sealed part {n}")
text = base64.b64decode(sealed.read_text()).decode()
out = PARTS / f"PART_{n}.md"
out.write_text(text)
print(text)
print(f"\n(saved to {out})")
