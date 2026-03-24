#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read stdin and write it to a file as UTF-8."
    )
    parser.add_argument("path", help="Destination file path")
    args = parser.parse_args()

    data = sys.stdin.read().lstrip("\ufeff").replace("\r\n", "\n")
    with Path(args.path).open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
