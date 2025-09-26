"""Utilities for synthesising a short literature review."""
from __future__ import annotations

import re
from collections import defaultdict
from datetime import datetime
from typing import Dict, Iterable, List

from .data_sources import Article


THEME_KEYWORDS: Dict[str, List[str]] = {
    "Health impacts": [
        "mortality",
        "morbidity",
        "cardio",
        "respir",
        "asthma",
        "hospital",
        "birth",
        "pregnan",
        "cancer",
        "disease",
        "inflammation",
    ],
    "Exposure assessment": [
        "exposure",
        "monitor",
        "model",
        "satellite",
        "sensor",
        "measurement",
        "remote",
        "spatial",
        "pm2.5",
        "pm10",
        "no2",
    ],
    "Sources and chemistry": [
        "source",
        "emission",
        "chemical",
        "composition",
        "secondary",
        "ozone",
        "aerosol",
    ],
    "Policy and mitigation": [
        "policy",
        "mitigation",
        "intervention",
        "regulation",
        "management",
        "control",
        "urban planning",
    ],
}


def build_literature_review(articles: Iterable[Article]) -> str:
    """Constructs a narrative literature review from the supplied articles."""
    article_list = [a for a in articles if a]
    if not article_list:
        return "No recent air pollution studies were retrieved."

    article_list.sort(key=lambda a: a.pub_date or datetime.min, reverse=True)

    earliest = min((a.pub_date for a in article_list if a.pub_date), default=None)
    latest = max((a.pub_date for a in article_list if a.pub_date), default=None)

    references = {article.identifier: idx + 1 for idx, article in enumerate(article_list)}

    sections: Dict[str, List[Article]] = defaultdict(list)
    for article in article_list:
        sections[_classify_article(article)].append(article)

    intro_lines: List[str] = []
    intro_lines.append("Literature Review: Recent Evidence on Air Pollution")
    if latest and earliest:
        intro_lines.append(
            f"This review synthesises {len(article_list)} peer-reviewed studies on air pollution "
            f"published between {earliest.date()} and {latest.date()}."
        )
    else:
        intro_lines.append(
            f"This review synthesises {len(article_list)} peer-reviewed studies on air pollution published within the last week."
        )
    intro_lines.append(
        "The synthesis highlights methodological advances, emerging health evidence, and policy-relevant findings from multiple bibliographic sources, including PubMed and Crossref-indexed journals."
    )

    body_lines: List[str] = []

    for theme, items in sections.items():
        body_lines.append(f"\n{theme}")
        for article in items:
            idx = references.get(article.identifier)
            summary = _summarise_article(article)
            body_lines.append(f"[{idx}] {summary}")

    reference_lines = ["\nReferences"]
    for article in article_list:
        idx = references[article.identifier]
        citation = article.short_citation()
        link = article.url or (f"https://doi.org/{article.doi}" if article.doi else "")
        if link:
            reference_lines.append(f"[{idx}] {citation} {link}")
        else:
            reference_lines.append(f"[{idx}] {citation}")

    return "\n".join(intro_lines + body_lines + reference_lines)


def _classify_article(article: Article) -> str:
    text = f"{article.title.lower()} {article.abstract.lower()}"
    best_theme = "Cross-cutting insights"
    best_score = 0

    for theme, keywords in THEME_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > best_score:
            best_score = score
            best_theme = theme

    return best_theme


def _summarise_article(article: Article) -> str:
    sentences = _split_sentences(article.abstract or "")
    if sentences:
        summary = " ".join(sentences[:2])
    else:
        summary = f"{article.title.strip()} discusses air pollution dynamics but no abstract was available."

    parts = [summary.rstrip("."), "Key details:"]
    details = []
    if article.journal:
        details.append(f"journal={article.journal}")
    if article.pub_date:
        details.append(f"date={article.pub_date.date()}")
    if article.doi:
        details.append(f"doi={article.doi}")
    if details:
        parts.append("; ".join(details))

    return " ".join(parts).strip()


def _split_sentences(text: str) -> List[str]:
    clean = re.sub(r"\s+", " ", text).strip()
    if not clean:
        return []
    # Simple sentence splitter that respects abbreviations trivially.
    sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", clean)
    return [s.strip() for s in sentences if s.strip()]
