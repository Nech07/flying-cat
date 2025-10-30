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
    return parser.parse_args()


def format_tags(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [chunk.strip() for chunk in raw.split(",") if chunk.strip()]


def build_front_matter(args: argparse.Namespace, date: dt.date, slug: str) -> str:
    def quote(value: str) -> str:
        escaped = value.replace('"', r"\"")
        return f'"{escaped}"'

    def value_or_default(raw: str | None, default: str) -> str:
        return raw.strip() if raw else default

    lines = ["---"]
    lines.append(f'title: {quote(args.title)}')
    lines.append(f'paper_title: {quote(value_or_default(args.paper_title, args.title))}')
    lines.append(f'paper_authors: {quote(value_or_default(args.authors, "TODO"))}')
    lines.append(f'paper_venue: {quote(value_or_default(args.venue, "TODO"))}')
    year_value = args.year if args.year else f"{date.year}"
    lines.append(f"paper_year: {year_value}")
    lines.append(f'paper_link: {quote(value_or_default(args.paper_link, "https://"))}')
    if args.paper_pdf:
        lines.append(f'paper_pdf: {quote(value_or_default(args.paper_pdf, "https://"))}')
    lines.append(f'paper_code: {quote(value_or_default(args.paper_code, "https://"))}')
    tags = format_tags(args.tags)
    if tags:
        lines.append("paper_tags:")
        for tag in tags:
            lines.append(f"  - {tag}")
    else:
        lines.append("paper_tags:")
        lines.append("  - TODO")
    lines.append("---")
    return "\n".join(lines)


def build_body() -> str:
    return dedent(
        """
        ## Main concept

        TODO

        ## Main advantages

        TODO

        ## Experiments results

        TODO

        ## Practical model application

        TODO

        ## technical details

        TODO

        ## Limitations

        TODO

        ## Future Directions

        TODO

        ## Overview

        TODO
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
