import pytest
from papercruncher.connectors.base import BaseConnector
from .mocks.mock_connector import MockConnector

def test_connector_interface():
    connector = MockConnector()
    papers = list(connector.fetch("test", max_results=2))
    assert len(papers) == 2
    for p in papers:
        assert isinstance(p, BaseConnector.__annotations__['fetch'].__args__[0])
