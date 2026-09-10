import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient, ASGITransport
from src.api.app import app, agent
from src.models.schemas import ResearchResponse, ToolResult, ToolType


@pytest.mark.asyncio
async def test_health_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_research_endpoint():
    transport = ASGITransport(app=app)

    mock_response = ResearchResponse(
        query="test query",
        steps=["step1"],
        tool_results=[],
        answer="test answer",
        confidence=0.5,
    )

    with patch.object(agent, "research", new_callable=AsyncMock) as mock_research:
        mock_research.return_value = mock_response
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/research", json={"query": "test query"})

    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "test query"
    assert data["answer"] == "test answer"


@pytest.mark.asyncio
async def test_tools_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/tools")

    assert response.status_code == 200
    data = response.json()
    assert "tools" in data
    assert len(data["tools"]) >= 3
    tool_names = [t["name"] for t in data["tools"]]
    assert "web_search" in tool_names
    assert "calculator" in tool_names


@pytest.mark.asyncio
async def test_code_analysis_endpoint():
    transport = ASGITransport(app=app)
    code = "def hello():\n    return 'hi'"
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/analyze/code", json={"code": code})

    assert response.status_code == 200
    data = response.json()
    assert "analysis" in data
    assert "hello" in data["analysis"]


@pytest.mark.asyncio
async def test_code_analysis_empty():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/analyze/code", json={})

    assert response.status_code == 200
    data = response.json()
    assert "error" in data
