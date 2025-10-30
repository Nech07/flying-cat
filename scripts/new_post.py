#!/usr/bin/env python3
"""Utility to scaffold a new paper note for the blog."""
from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "_posts"


def slugify(value: str) -> str:
    """Turn a title into a filesystem-friendly slug."""
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value)
    return value.strip("-") or "note"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", required=True, help="Blog post title")
    parser.add_argument("--paper-title", help="Original paper title")
    parser.add_argument("--authors", help="Primary authors")
    parser.add_argument("--venue", help="Conference or journal")
    parser.add_argument("--year", help="Publication year")
    parser.add_argument("--paper-link", help="Project or abstract link")
    parser.add_argument("--paper-pdf", help="Direct PDF link")
    parser.add_argument("--paper-code", help="Reference implementation link")
    parser.add_argument(
        "--tags",
        help="Comma separated tags such as 'transformers, attention'",
    )
    parser.add_argument(
        "--date",
        help="Publish date in YYYY-MM-DD (defaults to today)",
    )
    parser.add_argument(
        "--read-time",
        type=int,
        help="Estimated reading time in minutes",
    )
    return parser.parse_args()


def format_tags(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [chunk.strip() for chunk in raw.split(",") if chunk.strip()]


def build_front_matter(args: argparse.Namespace, date: dt.date, slug: str) -> str:
    lines = ["---"]
    lines.append(f'title: "{args.title}"')
    if args.paper_title:
        lines.append(f'paper_title: "{args.paper_title}"')
    if args.authors:
        lines.append(f'paper_authors: "{args.authors}"')
    if args.venue:
        lines.append(f'paper_venue: "{args.venue}"')
    if args.year:
        lines.append(f"paper_year: {args.year}")
    if args.paper_link:
        lines.append(f"paper_link: {args.paper_link}")
    if args.paper_pdf:
        lines.append(f"paper_pdf: {args.paper_pdf}")
    if args.paper_code:
        lines.append(f"paper_code: {args.paper_code}")
    tags = format_tags(args.tags)
    if tags:
        lines.append("paper_tags:")
        for tag in tags:
            lines.append(f"  - {tag}")
    if args.read_time:
        lines.append(f"read_time: {args.read_time}")
    lines.append("key_takeaways: |")
    lines.append("  - TODO")
    lines.append("further_reading: |")
    lines.append("  - TODO")
    lines.append("---")
    return "\n".join(lines)


def build_body() -> str:
    return dedent(
        """
        ## Why this paper

        TODO: Add the motivation for reading the paper and the main problem it solves.

        ## Model or method

        TODO: Summarize the core idea, architecture, or algorithmic steps.

        ## Results

        TODO: Capture the headline results or metrics you care about.

        ## Questions to revisit

        1. TODO
        2. TODO

        ## Implementation notes

        TODO: Document training tricks, hyperparameters, or pitfalls to remember.
        """
    ).strip() + "\n"


def main() -> None:
    args = parse_args()
    date = dt.date.fromisoformat(args.date) if args.date else dt.date.today()
    slug = slugify(args.title)
    filename = f"{date:%Y-%m-%d}-{slug}.md"
    target = POSTS_DIR / filename

    if target.exists():
        raise SystemExit(f"Refusing to overwrite existing file: {target}")

    front_matter = build_front_matter(args, date, slug)
    body = build_body()

    target.write_text(f"{front_matter}\n\n{body}", encoding="utf-8")
    print(f"Created {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
