import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.agent.planner import TaskPlanner, Plan, ToolCall
from src.models.schemas import ToolType


@pytest.fixture
def planner():
    return TaskPlanner()


@pytest.mark.asyncio
async def test_plan_with_preferred_tools(planner):
    preferred = [ToolType.WEB_SEARCH, ToolType.CALCULATOR]
    plan = await planner.plan("test query", preferred_tools=preferred)

    assert len(plan.tools) == 2
    assert plan.tools[0].tool == ToolType.WEB_SEARCH
    assert plan.tools[1].tool == ToolType.CALCULATOR
    assert "preferred" in plan.reasoning.lower()


@pytest.mark.asyncio
async def test_plan_keyword_selection_web_search(planner):
    plan = await planner.plan("search for Python tutorials")

    tool_types = [t.tool for t in plan.tools]
    assert ToolType.WEB_SEARCH in tool_types


@pytest.mark.asyncio
async def test_plan_keyword_selection_data_analysis(planner):
    plan = await planner.plan("analyze this csv data")

    tool_types = [t.tool for t in plan.tools]
    assert ToolType.DATA_ANALYSIS in tool_types


@pytest.mark.asyncio
async def test_plan_keyword_selection_calculator(planner):
    plan = await planner.plan("calculate the sum of numbers")

    tool_types = [t.tool for t in plan.tools]
    assert ToolType.CALCULATOR in tool_types


@pytest.mark.asyncio
async def test_plan_default_fallback(planner):
    plan = await planner.plan("random query with no keywords")

    assert len(plan.tools) >= 1
    assert plan.tools[0].tool == ToolType.WEB_SEARCH


@pytest.mark.asyncio
async def test_plan_with_llm_success(planner):
    mock_client = MagicMock()
    mock_client.chat.completions = AsyncMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = '{"tools": ["web_search", "calculator"], "reasoning": "test reasoning"}'
    mock_client.chat.completions.create.return_value = mock_response

    plan = await planner.plan_with_llm("search and calculate", mock_client)

    assert len(plan.tools) == 2
    assert plan.tools[0].tool == ToolType.WEB_SEARCH
    assert plan.tools[1].tool == ToolType.CALCULATOR
    assert plan.reasoning == "test reasoning"


@pytest.mark.asyncio
async def test_plan_with_llm_fallback(planner):
    mock_client = MagicMock()
    mock_client.chat.completions = AsyncMock()
    mock_client.chat.completions.create.side_effect = Exception("API error")

    plan = await planner.plan_with_llm("search for something", mock_client)

    assert len(plan.tools) >= 1
    assert "keyword fallback" in plan.reasoning.lower()
