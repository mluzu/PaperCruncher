import requests
from typing import Any, Dict, Iterable
from papercruncher.connectors.query import QuerySpec
from papercruncher.connectors.base import BaseConnector, PaperData


class SemanticScholarConnector(BaseConnector):
    API_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

    def build_query_params(self, spec: QuerySpec) -> Dict[str, Any]:
        return {
            "query": spec.keywords,
            "limit": spec.per_page,
            "offset": (spec.page - 1) * spec.per_page,
            "fields": ",".join(["title", "abstract", "authors" , 
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