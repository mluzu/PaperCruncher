import pytest
from papercruncher import BaseConnector
from mocks import MockConnector
from papercruncher import Paper


def test_connector_interface():
    connector = MockConnector()
    papers = list(connector.fetch("test", max_results=2))
    assert len(papers) == 2
    for p in papers:
        assert isinstance(p, Paper)
