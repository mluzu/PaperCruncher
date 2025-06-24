from datetime import date
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class QuerySpec(BaseModel):
    """
    Query specification. Same input for all connectors.
    """
    keywords: str = Field(..., description="search keywords")
    date_from: Optional[date] = Field(None, description="minimum date since publication")
    date_to: Optional[date] = Field(None, description="maximum date since publication")
    authors: Optional[List[str]] = Field(None, description="authors list")
    language: Optional[str] = Field(None, description="language")
    page: int = Field(1, ge=1, description="number of result pages from query")
    per_page: int = Field(10, ge=1, le=100, description="query results per page")
    filters: Optional[Dict[str, Any]] = Field(None, description="aditional filters")
