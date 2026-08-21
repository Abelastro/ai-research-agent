import asyncio
from src.agent.core import ResearchAgent
from src.models.schemas import ResearchRequest


async def main():
    agent = ResearchAgent()
    request = ResearchRequest(query="Analyze the latest trends in AI automation")
    response = await agent.research(request)
    print(f"Query: {response.query}")
    print(f"Answer: {response.answer}")
    print(f"Confidence: {response.confidence}")


if __name__ == "__main__":
    asyncio.run(main())
