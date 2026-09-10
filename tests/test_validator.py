import pytest
from src.agent.validator import validate_tool_results, calculate_confidence, filter_relevant_results
from src.models.schemas import ToolResult, ToolType


@pytest.mark.asyncio
async def test_validate_all_success():
    results = [
        ToolResult(tool=ToolType.WEB_SEARCH, input={"query": "test"}, output="results", success=True),
        ToolResult(tool=ToolType.CALCULATOR, input={"query": "1+1"}, output="2", success=True),
    ]
    validation = validate_tool_results(results)

    assert validation["valid"] is True
    assert validation["total"] == 2
    assert validation["successful"] == 2
    assert validation["failed"] == 0


@pytest.mark.asyncio
async def test_validate_partial_failure():
    results = [
        ToolResult(tool=ToolType.WEB_SEARCH, input={"query": "test"}, output="results", success=True),
        ToolResult(tool=ToolType.CALCULATOR, input={"query": "1/0"}, output="", success=False, error="division by zero"),
    ]
    validation = validate_tool_results(results)

    assert validation["valid"] is False
    assert validation["failed"] == 1
    assert len(validation["errors"]) == 1


@pytest.mark.asyncio
async def test_calculate_confidence():
    results = [
        ToolResult(tool=ToolType.WEB_SEARCH, input={"query": "test"}, output="results", success=True),
        ToolResult(tool=ToolType.CALCULATOR, input={"query": "1+1"}, output="2", success=True),
    ]
    confidence = calculate_confidence(results)
    assert confidence == 1.0


@pytest.mark.asyncio
async def test_calculate_confidence_partial():
    results = [
        ToolResult(tool=ToolType.WEB_SEARCH, input={"query": "test"}, output="results", success=True),
        ToolResult(tool=ToolType.CALCULATOR, input={"query": "1/0"}, output="", success=False, error="error"),
    ]
    confidence = calculate_confidence(results)
    assert 0.0 < confidence <= 0.5


@pytest.mark.asyncio
async def test_filter_relevant():
    results = [
        ToolResult(tool=ToolType.WEB_SEARCH, input={"query": "python"}, output="Python is a programming language", success=True),
        ToolResult(tool=ToolType.WEB_SEARCH, input={"query": "java"}, output="Java is another language", success=True),
    ]
    filtered = filter_relevant_results("python programming", results)
    assert len(filtered) >= 1


@pytest.mark.asyncio
async def test_validate_empty_results():
    validation = validate_tool_results([])
    assert validation["valid"] is False
    assert "No results" in validation["errors"][0]


@pytest.mark.asyncio
async def test_filter_empty_results():
    filtered = filter_relevant_results("test", [])
    assert filtered == []
