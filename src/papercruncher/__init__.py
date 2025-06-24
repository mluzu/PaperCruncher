from .models import BaseModel, Paper
from .connectors.connectors import BaseConnector
from .connectors.connectors import ArxivConnector
from .connectors.connectors import SemanticScholarConnector
from .connectors.query import QuerySpec


__all__ = [
    "BaseConnector", "ArxivConnector",
    "SemanticScholarConnector", "BaseModel", "Paper", "QuerySpec"
]
