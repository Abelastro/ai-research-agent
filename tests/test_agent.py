import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from src.models.schemas import ResearchRequest, ResearchResponse, ToolType, ToolResult
from src.agent.core import ResearchAgent


def test_research_request():
    request = ResearchRequest(query="test query")
    assert request.query == "test query"
    assert request.tools is None


def test_research_request_with_tools():
    request = ResearchRequest(
        query="test query", tools=[ToolType.WEB_SEARCH]
    )
    assert request.tools == [ToolType.WEB_SEARCH]


@pytest.mark.asyncio
async def test_agent_orchestration():
    agent = ResearchAgent()
    request = ResearchRequest(query="calculate 2 + 2")

    with patch.object(agent.executor, "execute") as mock_execute:
        mock_execute.return_value = ToolResult(
            tool=ToolType.CALCULATOR,
            input={"query": "calculate 2 + 2"},
            output="Calculation: 2 + 2 = 4",
            success=True,
        )
        response = await agent.research(request)

    assert isinstance(response, ResearchResponse)
    assert response.query == "calculate 2 + 2"
    assert len(response.tool_results) >= 1
    assert response.confidence > 0


@pytest.mark.asyncio
async def test_agent_confidence_calculation():
    agent = ResearchAgent()

    results = [
        ToolResult(tool=ToolType.WEB_SEARCH, input={}, output="results", success=True),
        ToolResult(tool=ToolType.CALCULATOR, input={}, output="42", success=True),
    ]
    confidence = agent._calculate_confidence(results)
    assert confidence == 1.0

    results_mixed = [
        ToolResult(tool=ToolType.WEB_SEARCH, input={}, output="results", success=True),
        ToolResult(tool=ToolType.CALCULATOR, input={}, output="", success=False, error="err"),
    ]
    confidence_mixed = agent._calculate_confidence(results_mixed)
    assert confidence_mixed < 1.0


@pytest.mark.asyncio
async def test_agent_no_tools():
    agent = ResearchAgent()
    request = ResearchRequest(query="random query no keywords")

    response = await agent.research(request)
    assert isinstance(response, ResearchResponse)
    assert len(response.tool_results) >= 1
