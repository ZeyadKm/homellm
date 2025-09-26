"""Command line interface for the air pollution literature agent."""
from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Sequence

from .agent import collect_recent_articles, load_email_settings, produce_literature_review
from .data_sources import DataSourceError
from .email_client import send_email


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile a weekly air pollution literature review.")
    parser.add_argument("--days", type=int, default=7, help="Number of days back to query (default: 7)")
    parser.add_argument("--max-pubmed", type=int, default=8, help="Maximum PubMed articles to include")
    parser.add_argument("--max-crossref", type=int, default=8, help="Maximum Crossref articles to include")
    parser.add_argument("--output", type=Path, help="Optional path to write the review text")
    parser.add_argument(
        "--skip-email",
        action="store_true",
        help="Generate the review without attempting to send email",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        articles = collect_recent_articles(
            days=args.days,
            max_pubmed=args.max_pubmed,
            max_crossref=args.max_crossref,
        )
    except DataSourceError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if not articles:
        print("No recent air pollution studies were retrieved.")
        return 0

    review = produce_literature_review(articles)

    print("Generated literature review:\n")
    print(review)

    if args.output:
        args.output.write_text(review, encoding="utf-8")
        print(f"\nSaved review to {args.output}")

    if not args.skip_email:
        try:
            settings = load_email_settings()
        except ValueError as exc:
            print(f"Email configuration error: {exc}", file=sys.stderr)
            return 1

        if settings:
            subject_date = datetime.utcnow().date().isoformat()
            subject = f"Weekly Air Pollution Literature Review ({subject_date})"
            try:
                send_email(settings, subject, review)
                print("Email sent successfully.")
            except Exception as exc:  # smtplib errors inherit from Exception
                print(f"Failed to send email: {exc}", file=sys.stderr)
                return 1
        else:
            print("Email settings were not provided; skipping email delivery.")

    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
