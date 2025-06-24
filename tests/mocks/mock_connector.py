from datetime import datetime
from typing import Any, Dict, Iterable
from papercruncher import BaseConnector
from papercruncher import Paper
from papercruncher import QuerySpec


class MockConnector(BaseConnector):
    def build_query_params(self, spec: QuerySpec) -> Dict[str, Any]:
        return spec.model_dump()

    def call_api(self, params: Dict[str, Any]) -> Any:
        # Mock no hace llamada externa; retorna los mismos 
        return params

    def parse_response(self, raw: Any):
        per_page = raw.get("per_page", 1)
        for i in range(per_page):
            yield {
                "title": f"Mock Title {i+1}",
                "summary": f"Summary for {raw.get('keywords')}",
                "authors": ",".join(raw.get("authors", []) or ["Mock Author"]),
                "published": raw.get("date_from") or raw.get("date_to") or None,
                "mock_params": raw
            }

    def fetch(self, query: str, max_results: int) -> Iterable[Paper]:
        papers=[]
        for i in range(max_results):
            papers.append(
                Paper(
                    id=1,
                    title=f"The {i}-th best paper on AI",
                    summary="",
                    authors="Jhon Doe",
                    published=datetime.today()
                )
            )
        return papers
