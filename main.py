#!/usr/bin/env python3
"""Till Firmware Do Us Part — a wedding vow for a device that keeps updating.

Writes the 130-character vow to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output/entry.txt), with no trailing newline.
"""

import os
import sys
import tempfile

ENTRY = (
    "I promise to love you through every update, every crash, "
    "and every factory reset \u2014 even if your firmware forgets "
    "why you chose me."
)


def entry_path(directory):
    return os.path.join(directory, "entry.txt")


def write_entry(directory):
    os.makedirs(directory, exist_ok=True)
    path = entry_path(directory)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(ENTRY)
    return path


def check_entry():
    if not 1 <= len(ENTRY) <= 200:
        print(f"entry is {len(ENTRY)} characters, outside the 1-200 window",
              file=sys.stderr)
        return False
    if ENTRY != ENTRY.strip() or "\n" in ENTRY:
        print("entry must be a single line with no surrounding whitespace",
              file=sys.stderr)
        return False
    print(f"entry OK: {len(ENTRY)} characters, "
          f"{len(ENTRY.encode('utf-8'))} bytes")
    return True


def self_test():
    if not check_entry():
        return False
    with tempfile.TemporaryDirectory() as tmp:
        path = write_entry(tmp)
        with open(path, "r", encoding="utf-8", newline="") as handle:
            back = handle.read()
        if back != ENTRY:
            print("round-trip mismatch", file=sys.stderr)
            return False
        print("self-test OK: byte-identical write/read round-trip")
    return True


def main(argv):
    if "--check" in argv:
        return 0 if check_entry() else 1
    if "--self-test" in argv:
        return 0 if self_test() else 1
    directory = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = write_entry(directory)
    with open(path, "r", encoding="utf-8", newline="") as handle:
        if handle.read() != ENTRY:
            print("verification failed: entry.txt differs", file=sys.stderr)
            return 1
    print(f"wrote {path} ({len(ENTRY)} characters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
