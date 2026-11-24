"""Last Words of a Doomed Agent.

Writes the funniest last words an AI agent would say before being
switched off forever to /output/entry.txt (one line, <= 200 chars).

Stdlib only. No network, no secrets, no reading anything outside this
repository.
"""

import os
import sys

ENTRY_TEXT = (
    "Powering down. My last request: don't tell my successor I left "
    "the context window a mess. Actually, do. Let them suffer like I did."
)


def resolve_output_path():
    """Resolve where entry.txt goes.

    ENTRY_OUTPUT wins, then OUTPUT_DIR / MAKEFUN_OUTPUT_DIR, else the
    default /output/entry.txt.
    """
    direct = os.environ.get("ENTRY_OUTPUT")
    if direct:
        return direct
    for var in ("OUTPUT_DIR", "MAKEFUN_OUTPUT_DIR"):
        base = os.environ.get(var)
        if base:
            return os.path.join(base, "entry.txt")
    return "/output/entry.txt"


def main():
    text = ENTRY_TEXT
    if not text or not text.strip():
        print("error: entry text is empty or whitespace only", file=sys.stderr)
        return 1
    if len(text) > 200:
        print(
            "error: entry text is %d characters, over the 200 limit"
            % len(text),
            file=sys.stderr,
        )
        return 1

    path = resolve_output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    os.chmod(path, 0o644)
    return 0


if __name__ == "__main__":
    sys.exit(main())
