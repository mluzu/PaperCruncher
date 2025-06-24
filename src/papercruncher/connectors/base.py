from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable
from papercruncher.connectors.query import QuerySpec
from papercruncher.models import Paper


PaperData = Dict[str, Any]


class BaseConnector(ABC):
    """
    Connector interface.
    Fetch flow steps:
      1. build_query_params
      2. call_api
      3. parse_response
    """

    @abstractmethod
    def build_query_params(self, spec: QuerySpec) -> Dict[str, Any]:
        """Builds query parameters from QuerySpec."""
        ...

    @abstractmethod
    def call_api(self, params: Dict[str, Any]) -> Any:
        """Performs the API call (JSON, XML, etc.)."""
        ...

    @abstractmethod
    def parse_response(self, raw: Any) -> Iterable[PaperData]:
        """Parses the response."""
        ...

    def fetch(self, spec: QuerySpec) -> Iterable[PaperData]:
        """
        Sequence query steps
        """
        params = self.build_query_params(spec)
        raw = self.call_api(params)
        yield from self.parse_response(raw)
