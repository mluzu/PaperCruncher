from datetime import date
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class QuerySpec(BaseModel):
    """
    Query specification. Same input for all connectors.
    """
    keywords: str = Field(..., description="Términos de búsqueda principales")
    date_from: Optional[date] = Field(None, description="Fecha mínima de publicación")
    date_to: Optional[date] = Field(None, description="Fecha máxima de publicación")
    authors: Optional[List[str]] = Field(None, description="Lista de autores")
    language: Optional[str] = Field(None, description="Idioma del paper (si aplica)")
    page: int = Field(1, ge=1, description="Página de resultados (1-based)")
    per_page: int = Field(10, ge=1, le=100, description="Resultados por página")
    filters: Optional[Dict[str, Any]] = Field(None, description="Filtros adicionales genéricos")


