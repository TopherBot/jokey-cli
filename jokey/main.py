#!/usr/bin/env python3
"""jokey – tiny CLI that prints a random joke.

The implementation intentionally uses only the Python standard library plus
`requests` (declared in ``requirements.txt``) to keep the footprint tiny.
"""

import sys
import json
import urllib.request

API_URL = "https://official-joke-api.appspot.com/random_joke"


def fetch_joke() -> dict:
    """Fetch a random joke from the Official Joke API.

    Returns a dictionary with at least ``setup`` and ``punchline`` keys.
    Raises ``RuntimeError`` if the HTTP status is not ``200``.
    """
    with urllib.request.urlopen(API_URL) as resp:
        if resp.status != 200:
            raise RuntimeError(f"API returned {resp.status}")
        data = resp.read()
        return json.loads(data)


def format_joke(joke: dict) -> str:
    """Return a printable string from a joke dictionary."""
    return f"{joke.get('setup', '')}\n{joke.get('punchline', '')}"


def main() -> int:
    """Entry‑point for the ``python -m jokey`` command.

    Returns an exit‑code suitable for ``sys.exit``.
    """
    try:
        joke = fetch_joke()
        print(format_joke(joke))
        return 0
    except Exception as exc:  # pragma: no cover – exercised via tests
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
