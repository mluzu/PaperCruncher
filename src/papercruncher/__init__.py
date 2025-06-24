from .models import BaseModel, Paper
from .connectors.base import BaseConnector
from .connectors.query import QuerySpec
from .connectors.connector_arxiv import ArxivConnector
from .connectors.connector_semantic_scholar import SemanticScholarConnector

__all__ = [
    "BaseConnector", "ArxivConnector",
    "SemanticScholarConnector", "BaseModel", "Paper", "QuerySpec"
]
