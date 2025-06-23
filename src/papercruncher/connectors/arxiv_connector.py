import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Iterable
from papercruncher.connectors.base import BaseConnector
from papercruncher.models import Paper

class ArxivConnector(BaseConnector):
    """
    ArxivConnector implements BaseConnector for arXiv's API.
    """
    API_URL = "http://export.arxiv.org/api/query"

    def fetch(self, query: str, max_results: int = 50) -> Iterable[Paper]:
        params = {
            "search_query": query,
            "start": 0,
            "max_results": max_results
        }
        resp = requests.get(self.API_URL, params=params, timeout=10)
        resp.raise_for_status()
        xml = resp.text

        ns = {"atom": "http://www.w3.org/2005/Atom"}
        root = ET.fromstring(xml)

        for entry in root.findall("atom:entry", ns):
            title = entry.find("atom:title", ns).text.strip()
            summary = entry.find("atom:summary", ns).text.strip()
            authors = ", ".join(
                a.find("atom:name", ns).text
                for a in entry.findall("atom:author", ns)
            )
            published_str = entry.find("atom:published", ns).text
            # arXiv usa ISO 8601, e.g. "2025-06-23T12:34:56Z"
            published = datetime.fromisoformat(published_str.replace("Z", "+00:00"))

            yield Paper(
                title=title,
                summary=summary,
                authors=authors,
                published=published
            )
