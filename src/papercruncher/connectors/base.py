from abc import ABC, abstractmethod
from typing import Iterable
from papercruncher.models import Paper


class BaseConnector(ABC):
    @abstractmethod
    def fetch(self, query: str, max_results: int) -> Iterable[Paper]:
        """
        Performs queries and retrieves papers from the online repository.
        The result is returned as a list of paper objects
        """
        pass
