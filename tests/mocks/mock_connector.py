from datetime import datetime
from typing import Iterable
from papercruncher import BaseConnector
from papercruncher import Paper


class MockConnector(BaseConnector):

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
