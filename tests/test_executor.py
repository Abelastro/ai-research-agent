import pytest
from unittest.mock import AsyncMock
from src.agent.executor import ToolExecutor
from src.agent.planner import ToolCall
from src.models.schemas import ToolType


@pytest.fixture
def executor():
    return ToolExecutor()


@pytest.mark.asyncio
async def test_execute_calculator(executor):
    call = ToolCall(tool=ToolType.CALCULATOR, parameters={"query": "2 + 2"})
    result = await executor.execute(call)

    assert result.success is True
    assert "Calculation" in result.output
    assert result.tool == ToolType.CALCULATOR


@pytest.mark.asyncio
async def test_execute_web_search(executor):
    call = ToolCall(tool=ToolType.WEB_SEARCH, parameters={"query": "test search"})
    result = await executor.execute(call)

    assert result.success is True
    assert "Search results" in result.output


@pytest.mark.asyncio
async def test_execute_data_analysis(executor):
    csv_data = "name,age\nAlice,30\nBob,25"
    call = ToolCall(
        tool=ToolType.DATA_ANALYSIS,
        parameters={"query": "analyze", "csv_data": csv_data},
    )
    result = await executor.execute(call)

    assert result.success is True
    assert "Data Analysis" in result.output


@pytest.mark.asyncio
async def test_execute_file_reader(executor):
    call = ToolCall(tool=ToolType.FILE_READER, parameters={"file_path": "/dev/null"})
    result = await executor.execute(call)

    assert result.success is True


@pytest.mark.asyncio
async def test_execute_unknown_tool():
    executor = ToolExecutor()
    executor.tool_map.pop(ToolType.WEB_SEARCH, None)
    call = ToolCall(tool=ToolType.WEB_SEARCH, parameters={"query": "test"})
    result = await executor.execute(call)

    assert result.success is False
    assert "not implemented" in result.error


@pytest.mark.asyncio
async def test_execute_with_error(executor):
    original_func = executor.tool_map[ToolType.WEB_SEARCH]
    executor.tool_map[ToolType.WEB_SEARCH] = AsyncMock(side_effect=Exception("test error"))

    call = ToolCall(tool=ToolType.WEB_SEARCH, parameters={"query": "test"})
    result = await executor.execute(call)

    assert result.success is False
    assert "test error" in result.error

    executor.tool_map[ToolType.WEB_SEARCH] = original_func
