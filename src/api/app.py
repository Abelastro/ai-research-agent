from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from ..models.schemas import ResearchRequest, ResearchResponse
from ..agent.core import ResearchAgent
from ..tools.code_analyzer import analyze_python_code
import json

app = FastAPI(
    title="AI Research Agent",
    description="AI agent for research queries with tool calling",
    version="0.1.0",
)

agent = ResearchAgent()


@app.post("/research", response_model=ResearchResponse)
async def research(request: ResearchRequest):
    return await agent.research(request)


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/research/stream")
async def research_stream(request: ResearchRequest):
    async def generate():
        async for event in agent.research_stream(request.query):
            yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.get("/tools")
async def list_tools():
    return {
        "tools": [
            {"name": "web_search", "description": "Search the web for information"},
            {"name": "data_analysis", "description": "Analyze CSV data and compute statistics"},
            {"name": "calculator", "description": "Perform mathematical calculations"},
            {"name": "file_reader", "description": "Read files, CSVs, and list directories"},
            {"name": "code_analyzer", "description": "Analyze Python code for structure and complexity"},
        ]
    }


@app.post("/analyze/code")
async def code_analysis(payload: dict):
    code = payload.get("code", "")
    if not code:
        return {"error": "No code provided"}
    result = await analyze_python_code(code)
    return {"analysis": result}
