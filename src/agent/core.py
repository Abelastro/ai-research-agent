from typing import Optional
from ..models.schemas import ResearchRequest, ResearchResponse, ToolResult, ToolType
from .planner import TaskPlanner
from .executor import ToolExecutor


class ResearchAgent:
    def __init__(self, api_key: Optional[str] = None):
        self.planner = TaskPlanner(api_key=api_key)
        self.executor = ToolExecutor()

    async def research(self, request: ResearchRequest) -> ResearchResponse:
        steps = []

        steps.append("Analyzing query intent")
        plan = await self.planner.plan(request.query, request.tools)

        steps.append(f"Executing {len(plan.tools)} tools")
        tool_results = []
        for tool_call in plan.tools:
            result = await self.executor.execute(tool_call)
            tool_results.append(result)

        steps.append("Generating response")
        answer = await self._generate_answer(request.query, tool_results)

        return ResearchResponse(
            query=request.query,
            steps=steps,
            tool_results=tool_results,
            answer=answer,
            confidence=self._calculate_confidence(tool_results),
        )

    async def _generate_answer(
        self, query: str, results: list[ToolResult]
    ) -> str:
        successful_results = [r for r in results if r.success]
        if not successful_results:
            return "Unable to process the query. No tools returned valid results."

        summary_parts = []
        for result in successful_results:
            summary_parts.append(f"[{result.tool.value}] {result.output}")

        return "\n\n".join(summary_parts)

    def _calculate_confidence(self, results: list[ToolResult]) -> float:
        if not results:
            return 0.0
        successful = sum(1 for r in results if r.success)
        return successful / len(results)
