from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable
from papercruncher.connectors.query import QuerySpec
from papercruncher.models import Paper


PaperData = Dict[str, Any]


class BaseConnector(ABC):
    """
    Interfaz de conector genérico para fuentes de papers.
    Define el flujo template method para fetch:
      1. build_query_params
      2. call_api
      3. parse_response
    """

    @abstractmethod
    def build_query_params(self, spec: QuerySpec) -> Dict[str, Any]:
        """Construye los parámetros de consulta HTTP a partir de QuerySpec."""
        ...

    @abstractmethod
    def call_api(self, params: Dict[str, Any]) -> Any:
        """Ejecuta la llamada HTTP y devuelve la respuesta cruda (JSON, XML, etc.)."""
        ...

    @abstractmethod
    def parse_response(self, raw: Any) -> Iterable[PaperData]:
        """Parsea la respuesta cruda en un iterable de diccionarios intermedios."""
        ...

    def fetch(self, spec: QuerySpec) -> Iterable[PaperData]:
        """
        Método template: orquesta la extracción desde la fuente.
        """
        params = self.build_query_params(spec)
        raw = self.call_api(params)
        yield from self.parse_response(raw)
