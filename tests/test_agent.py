import pytest
from src.models.schemas import ResearchRequest, ToolType


def test_research_request():
    request = ResearchRequest(query="test query")
    assert request.query == "test query"
    assert request.tools is None


def test_research_request_with_tools():
    request = ResearchRequest(
        query="test query", tools=[ToolType.WEB_SEARCH]
    )
    assert request.tools == [ToolType.WEB_SEARCH]
