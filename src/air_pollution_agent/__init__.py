"""Air pollution literature agent package."""
from .agent import collect_recent_articles, load_email_settings, produce_literature_review
from .data_sources import Article, DataSourceError

__all__ = [
    "Article",
    "DataSourceError",
    "collect_recent_articles",
    "load_email_settings",
    "produce_literature_review",
]
