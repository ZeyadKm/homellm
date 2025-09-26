"""Data source clients for retrieving recent air pollution studies."""
from __future__ import annotations

import os
import textwrap
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional
from urllib.parse import quote

import requests
from xml.etree import ElementTree


RELEVANCE_KEYWORDS = [
    "air pollution",
    "air-quality",
    "air quality",
    "particulate",
    "pm2.5",
    "pm10",
    "nitrogen dioxide",
    "no2",
    "sulfur dioxide",
    "so2",
    "ozone",
    "black carbon",
    "smog",
    "smoke",
    "aerosol",
    "emission",
]


@dataclass
class Article:
    """Represents a scholarly article."""

    source: str
    identifier: str
    title: str
    abstract: str
    journal: Optional[str]
    pub_date: Optional[datetime]
    authors: List[str]
    doi: Optional[str]
    url: Optional[str]

    def short_citation(self) -> str:
        """Returns a simple one-line citation for references."""
        author_part = ", ".join(self.authors[:3]) or "Unknown"  # prune to keep neat
        if len(self.authors) > 3:
            author_part += " et al."
        year = f"{self.pub_date.year}" if self.pub_date else "n.d."
        journal_part = f" {self.journal}" if self.journal else ""
        return f"{author_part} ({year}). {self.title}.{journal_part}".strip()


class DataSourceError(RuntimeError):
    """Raised when a data source cannot be queried successfully."""


def _user_agent() -> str:
    contact_email = os.environ.get("AIR_AGENT_CONTACT_EMAIL", "air.pollution.agent@example.com")
    return f"air-pollution-agent/1.0 ({contact_email})"


def fetch_pubmed_articles(days: int = 7, retmax: int = 8) -> List[Article]:
    """Fetches recent air pollution publications from PubMed."""
    base_params = {
        "db": "pubmed",
        "term": "air pollution",
        "reldate": str(days),
        "datetype": "pdat",
        "retmax": str(retmax),
        "retmode": "json",
        "sort": "pub+date",
        "tool": "air_pollution_agent",
        "email": os.environ.get("AIR_AGENT_CONTACT_EMAIL", "air.pollution.agent@example.com"),
    }

    headers = {"User-Agent": _user_agent()}

    try:
        search_resp = requests.get(
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
            params=base_params,
            headers=headers,
            timeout=30,
        )
        search_resp.raise_for_status()
    except requests.RequestException as exc:
        raise DataSourceError("Failed querying PubMed search endpoint") from exc

    idlist = search_resp.json().get("esearchresult", {}).get("idlist", [])
    if not idlist:
        return []

    fetch_params = {
        "db": "pubmed",
        "id": ",".join(idlist),
        "retmode": "xml",
        "tool": "air_pollution_agent",
        "email": os.environ.get("AIR_AGENT_CONTACT_EMAIL", "air.pollution.agent@example.com"),
    }

    try:
        fetch_resp = requests.get(
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi",
            params=fetch_params,
            headers=headers,
            timeout=30,
        )
        fetch_resp.raise_for_status()
    except requests.RequestException as exc:
        raise DataSourceError("Failed retrieving PubMed summaries") from exc

    tree = ElementTree.fromstring(fetch_resp.content)
    articles: List[Article] = []

    for article_node in tree.findall(".//PubmedArticle"):
        article = _parse_pubmed_article(article_node)
        if article:
            articles.append(article)

    return articles


def _parse_pubmed_article(node: ElementTree.Element) -> Optional[Article]:
    medline = node.find("MedlineCitation")
    if medline is None:
        return None

    article = medline.find("Article")
    if article is None:
        return None

    title = _get_text(article.find("ArticleTitle")) or "Untitled"
    abstract = "\n".join(
        filter(None, [
            textwrap.dedent(_get_text(ab))
            for ab in article.findall("Abstract/AbstractText")
        ])
    )
    journal = _get_text(article.find("Journal/Title"))
    pub_date = _parse_pubmed_pub_date(article)
    authors = _parse_pubmed_authors(article)
    article_id = _get_text(medline.find("PMID")) or ""
    doi = None
    url = None

    for id_node in article.findall("ELocationID"):
        if id_node.get("EIdType") == "doi":
            doi = _get_text(id_node)
            break

    if not doi:
        for id_node in article.findall("ArticleIdList/ArticleId"):
            if id_node.get("IdType") == "doi":
                doi = _get_text(id_node)
                break

    if doi:
        url = f"https://doi.org/{quote(doi)}"
    elif article_id:
        url = f"https://pubmed.ncbi.nlm.nih.gov/{article_id}/"

    return Article(
        source="PubMed",
        identifier=article_id,
        title=title.strip(),
        abstract=abstract.strip(),
        journal=journal.strip() if journal else None,
        pub_date=pub_date,
        authors=authors,
        doi=doi.strip() if doi else None,
        url=url,
    )


def _parse_pubmed_authors(article: ElementTree.Element) -> List[str]:
    authors = []
    for author in article.findall("AuthorList/Author"):
        last = _get_text(author.find("LastName"))
        fore = _get_text(author.find("ForeName")) or _get_text(author.find("Initials"))
        if last and fore:
            authors.append(f"{last} {fore}")
        elif last or fore:
            authors.append(last or fore)
    return authors


def _parse_pubmed_pub_date(article: ElementTree.Element) -> Optional[datetime]:
    def parse_date(parts: List[str]) -> Optional[datetime]:
        try:
            return datetime.strptime("-".join(parts), "%Y-%m-%d")
        except ValueError:
            try:
                return datetime.strptime("-".join(parts[:2]), "%Y-%m")
            except ValueError:
                try:
                    return datetime.strptime(parts[0], "%Y")
                except ValueError:
                    return None

    article_date = article.find("ArticleDate")
    if article_date is not None:
        parts = [
            _get_text(article_date.find("Year")),
            _get_text(article_date.find("Month")),
            _get_text(article_date.find("Day")),
        ]
        parts = [p for p in parts if p]
        if parts:
            parsed = parse_date(parts)
            if parsed:
                return parsed

    journal_issue = article.find("Journal/JournalIssue/PubDate")
    if journal_issue is not None:
        parts = [
            _get_text(journal_issue.find("Year")),
            _get_text(journal_issue.find("Month")),
            _get_text(journal_issue.find("Day")),
        ]
        parts = [p for p in parts if p]
        if parts:
            parsed = parse_date(parts)
            if parsed:
                return parsed

    return None


def _get_text(node: Optional[ElementTree.Element]) -> Optional[str]:
    if node is None:
        return None
    text = "".join(node.itertext()).strip()
    return text or None


def fetch_crossref_articles(days: int = 7, rows: int = 8) -> List[Article]:
    """Fetches recent air pollution publications indexed by Crossref."""
    today = datetime.utcnow().date()
    start = today - timedelta(days=days)

    params = {
        "filter": f"from-pub-date:{start.isoformat()},until-pub-date:{today.isoformat()},type:journal-article",
        "sort": "published",
        "order": "desc",
        "rows": str(rows),
        "query": "air pollution",
    }

    headers = {"User-Agent": _user_agent()}

    try:
        resp = requests.get(
            "https://api.crossref.org/works",
            params=params,
            headers=headers,
            timeout=30,
        )
        resp.raise_for_status()
    except requests.RequestException as exc:
        raise DataSourceError("Failed querying Crossref") from exc

    data = resp.json().get("message", {}).get("items", [])
    articles: List[Article] = []

    for idx, item in enumerate(data):
        doi = item.get("DOI")
        url = item.get("URL")
        title = "; ".join(item.get("title", [])) or "Untitled"
        journal_titles = item.get("container-title", [])
        journal = journal_titles[0] if journal_titles else None
        issued = item.get("issued", {}).get("date-parts", [])
        pub_date = None
        if issued and issued[0]:
            parts = issued[0] + [1] * (3 - len(issued[0]))
            try:
                pub_date = datetime(year=parts[0], month=parts[1], day=parts[2])
            except ValueError:
                pub_date = None

        authors_meta = item.get("author", [])
        authors = []
        for author in authors_meta:
            given = author.get("given")
            family = author.get("family")
            if given and family:
                authors.append(f"{family} {given}")
            elif family or given:
                authors.append(family or given)

        abstract = item.get("abstract") or ""
        abstract = _strip_crossref_abstract(abstract)

        text_blob = " ".join([title, abstract, " ".join(item.get("subject", []))]).lower()
        if not any(keyword in text_blob for keyword in RELEVANCE_KEYWORDS):
            continue

        articles.append(
            Article(
                source="Crossref",
                identifier=doi or f"crossref-{idx}",
                title=title.strip(),
                abstract=abstract.strip(),
                journal=journal.strip() if journal else None,
                pub_date=pub_date,
                authors=authors,
                doi=doi,
                url=url or (f"https://doi.org/{doi}" if doi else None),
            )
        )

    return articles


def _strip_crossref_abstract(raw: str) -> str:
    if not raw:
        return ""

    # Crossref abstracts may include simple HTML or JATS XML fragments.
    try:
        fragment = ElementTree.fromstring(raw)
        return " ".join(fragment.itertext()).strip()
    except ElementTree.ParseError:
        # Fallback: basic cleanup of HTML entities/tags.
        return (
            raw.replace("<jats:p>", " ")
            .replace("</jats:p>", " ")
            .replace("<p>", " ")
            .replace("</p>", " ")
            .replace("\n", " ")
            .strip()
        )
