from fastapi import FastAPI
from ..models.schemas import ResearchRequest, ResearchResponse
from ..agent.core import ResearchAgent

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
