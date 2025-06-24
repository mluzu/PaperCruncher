import pytest
from papercruncher import QuerySpec
from papercruncher import ArxivConnector


@pytest.fixture
def xml_response():
    return """
    <feed xmlns='http://www.w3.org/2005/Atom'>
      <entry>
        <title>Test Paper</title>
        <summary>Abstract</summary>
        <author><name>John Doe</name></author>
        <published>2025-01-01T00:00:00Z</published>
      </entry>
    </feed>
    """

def test_build_query_params():
    spec = QuerySpec(keywords="ai", page=2, per_page=5)
    params = ArxivConnector().build_query_params(spec)
    assert params["search_query"] == "all:ai"
    assert params["start"] == 5
    assert params["max_results"] == 5

def test_parse_response(requests_mock, xml_response):
    spec = QuerySpec(keywords="ai")
    mock = requests_mock.get(ArxivConnector.API_URL, text=xml_response)
    connector = ArxivConnector()
    data = list(connector.fetch(spec))
    assert len(data) == 1
    item = data[0]
    assert item["title"] == "Test Paper"
    assert item["authors"] == "John Doe"
    assert item["published"].year == 2025
