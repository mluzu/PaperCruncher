import pytest
from papercruncher import QuerySpec
from papercruncher import SemanticScholarConnector

@pytest.fixture
def json_response():
    return {"data": [
        {"title": "SS Test", "abstract": "Abs", "authors": [{"name":"A"}], "year": 2024, "url": "http://"}
    ]}

def test_build_query_params_ss():
    spec = QuerySpec(keywords="ml", page=1, per_page=3)
    params = SemanticScholarConnector().build_query_params(spec)
    assert params["query"] == "ml"
    assert params["limit"] == 3

def test_parse_response_ss(requests_mock, json_response):
    spec = QuerySpec(keywords="ml")
    requests_mock.get(SemanticScholarConnector.API_URL, json=json_response)
    data = list(SemanticScholarConnector().fetch(spec))
    assert data[0]["title"] == "SS Test"
    assert "authors" in data[0]