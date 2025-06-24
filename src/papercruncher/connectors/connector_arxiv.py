import requests
from typing import Any, Dict, Iterable
import xml.etree.ElementTree as ET
from datetime import datetime
from papercruncher.connectors.query import QuerySpec
from papercruncher.connectors.base import BaseConnector, PaperData
from papercruncher.models import Paper


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
