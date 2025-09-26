"""Core orchestration logic for the air pollution literature agent."""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence

from .data_sources import Article, fetch_crossref_articles, fetch_pubmed_articles
from .review_builder import build_literature_review


@dataclass
class EmailSettings:
    host: str
    port: int
    sender: str
    recipients: Sequence[str]
    username: Optional[str] = None
    password: Optional[str] = None
    use_tls: bool = True


def collect_recent_articles(
    *,
    days: int = 7,
    max_pubmed: int = 8,
    max_crossref: int = 8,
) -> List[Article]:
    pubmed = fetch_pubmed_articles(days=days, retmax=max_pubmed)
    crossref = fetch_crossref_articles(days=days, rows=max_crossref)

    articles: List[Article] = []
    seen_doi = set()
    seen_titles = set()

    for entry in pubmed + crossref:
        doi_key = entry.doi.lower() if entry.doi else None
        title_key = _normalise_title(entry.title)

        if doi_key and doi_key in seen_doi:
            continue
        if title_key in seen_titles:
            continue

        if doi_key:
            seen_doi.add(doi_key)
        seen_titles.add(title_key)
        articles.append(entry)

    return articles


def produce_literature_review(articles: Iterable[Article]) -> str:
    return build_literature_review(list(articles))


def load_email_settings() -> Optional[EmailSettings]:
    host = os.environ.get("AIR_AGENT_SMTP_HOST")
    recipients = os.environ.get("AIR_AGENT_EMAIL_TO")
    if not host or not recipients:
        return None

    port = int(os.environ.get("AIR_AGENT_SMTP_PORT", "587"))
    username = os.environ.get("AIR_AGENT_SMTP_USER")
    password = os.environ.get("AIR_AGENT_SMTP_PASSWORD")
    sender = os.environ.get("AIR_AGENT_EMAIL_FROM") or username or ""
    if not sender:
        raise ValueError("Email sender must be provided via AIR_AGENT_EMAIL_FROM or AIR_AGENT_SMTP_USER")

    addresses = [addr.strip() for addr in recipients.split(",") if addr.strip()]
    if not addresses:
        raise ValueError("At least one email recipient must be specified in AIR_AGENT_EMAIL_TO")

    return EmailSettings(
        host=host,
        port=port,
        sender=sender,
        recipients=addresses,
        username=username,
        password=password,
        use_tls=os.environ.get("AIR_AGENT_SMTP_USE_TLS", "true").lower() != "false",
    )


def _normalise_title(title: str) -> str:
    return " ".join(title.lower().split())
