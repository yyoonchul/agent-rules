#!/usr/bin/env python3
"""Convert a single input file to Markdown using Microsoft's markitdown.

Usage:
    python3 convert.py <input> [--output <path>] [--stdout]

Exit codes:
    0 - success
    2 - usage error
    3 - markitdown not installed
    4 - input not found
    5 - conversion failed
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _load_markitdown():
    try:
        from markitdown import MarkItDown  # type: ignore
    except ImportError:
        sys.stderr.write(
            "error: markitdown is not installed.\n"
            "install with: pip install 'markitdown[all]'\n"
        )
        sys.exit(3)
    return MarkItDown


def convert(input_path: Path, output_path: Path | None, to_stdout: bool) -> Path | None:
    MarkItDown = _load_markitdown()
    md = MarkItDown()

    try:
        result = md.convert(str(input_path))
    except Exception as exc:  # noqa: BLE001
        sys.stderr.write(f"error: conversion failed: {exc}\n")
        sys.exit(5)

    text = result.text_content or ""

    if to_stdout:
        sys.stdout.write(text)
        return None

    if output_path is None:
        output_path = input_path.with_suffix(".md")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")
    return output_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Convert a file to Markdown via markitdown."
    )
    parser.add_argument("input", help="Input file path or URL (e.g., YouTube URL).")
    parser.add_argument(
        "--output",
        "-o",
        help="Output .md path. Defaults to <input>.md next to the source.",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Write Markdown to stdout instead of a file.",
    )
    args = parser.parse_args(argv)

    input_arg = args.input
    is_url = "://" in input_arg
    input_path = Path(input_arg)

    if not is_url and not input_path.exists():
        sys.stderr.write(f"error: input not found: {input_arg}\n")
        return 4

    output_path = Path(args.output) if args.output else None
    if args.stdout and args.output:
        sys.stderr.write("error: --stdout and --output are mutually exclusive\n")
        return 2

    written = convert(
        input_path=input_path if not is_url else Path(input_arg),
        output_path=output_path,
        to_stdout=args.stdout,
    )
    if written is not None:
        print(str(written))
    return 0


if __name__ == "__main__":
    sys.exit(main())
