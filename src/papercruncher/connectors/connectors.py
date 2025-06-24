from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, Iterable
import xml.etree.ElementTree as ET
import requests
from papercruncher.connectors.query import QuerySpec


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


class ArxivConnector(BaseConnector):
    API_URL = "http://export.arxiv.org/api/query"

    def build_query_params(self, spec: QuerySpec) -> Dict[str, Any]:
        q = f"all:{spec.keywords}"
        params = {
            "search_query": q,
            "start": (spec.page - 1) * spec.per_page,
            "max_results": spec.per_page
        }
        return params

    def call_api(self, params: Dict[str, Any]) -> Any:
        headers = {"User-Agent": "PaperCruncher/0.1"}
        resp = requests.get(
            self.API_URL,
            params=params,
            headers=headers,
            timeout=10
        )
        resp.raise_for_status()
        return resp.text

    def parse_response(self, raw: Any) -> Iterable[PaperData]:
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        root = ET.fromstring(raw)
        for entry in root.findall("atom:entry", ns):
            title = entry.find("atom:title", ns).text.strip()
            summary = entry.find("atom:summary", ns).text.strip()
            authors = ", ".join(
                a.find("atom:name", ns).text
                for a in entry.findall("atom:author", ns)
            )
            published_str = entry.find("atom:published", ns).text
            published = datetime.fromisoformat(published_str.replace("Z", "+00:00"))
            yield {
                "title": title,
                "summary": summary,
                "authors": authors,
                "published": published
            }


class SemanticScholarConnector(BaseConnector):
    API_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

    def build_query_params(self, spec: QuerySpec) -> Dict[str, Any]:
        return {
            "query": spec.keywords,
            "limit": spec.per_page,
            "offset": (spec.page - 1) * spec.per_page,
            "fields": ",".join(["title", "abstract", "authors",
                                "year", "publicationTypes", "url"])
        }

    def call_api(self, params: Dict[str, Any]) -> Any:
        headers = {"User-Agent": "PaperCruncher/0.1"}
        resp = requests.get(
            self.API_URL,
            params=params,
            headers=headers,
            timeout=10
        )
        resp.raise_for_status()
        return resp.json()

    def parse_response(self, raw: Any) -> Iterable[PaperData]:
        for item in raw.get("data", []):
            authors = ", ".join(a.get("name", "")
                                for a in item.get("authors", []))
            yield {
                "title": item.get("title"),
                "summary": item.get("abstract"),
                "authors": authors,
                "published": item.get("year"),
                "url": item.get("url")
            }
