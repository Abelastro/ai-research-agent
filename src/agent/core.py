from typing import Optional, AsyncGenerator
from ..models.schemas import ResearchRequest, ResearchResponse, ToolResult, ToolType
from .planner import TaskPlanner
from .executor import ToolExecutor
from .validator import validate_tool_results, calculate_confidence, filter_relevant_results


class ResearchAgent:
    def __init__(self, **kwargs):
        self.planner = TaskPlanner(**kwargs)
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

    async def research_stream(self, query: str) -> AsyncGenerator[dict, None]:
        yield {"type": "step", "content": "Analyzing query intent"}
        plan = await self.planner.plan(query)

        yield {"type": "step", "content": f"Executing {len(plan.tools)} tools"}
        tool_results = []
        for tool_call in plan.tools:
            result = await self.executor.execute(tool_call)
            tool_results.append(result)
            yield {
                "type": "tool_result",
                "tool": result.tool.value,
                "success": result.success,
                "output": result.output if result.success else result.error,
            }

        yield {"type": "step", "content": "Generating response"}
        answer = await self._generate_answer(query, tool_results)

        yield {
            "type": "complete",
            "query": query,
            "answer": answer,
            "confidence": self._calculate_confidence(tool_results),
        }

    async def research_with_validation(self, request: ResearchRequest) -> ResearchResponse:
        steps = []

        steps.append("Analyzing query intent")
        plan = await self.planner.plan(request.query, request.tools)

        steps.append(f"Executing {len(plan.tools)} tools")
        tool_results = []
        for tool_call in plan.tools:
            result = await self.executor.execute(tool_call)
            tool_results.append(result)

        validation = validate_tool_results(tool_results)
        steps.append(f"Validation: {validation['successful']}/{validation['total']} tools succeeded")

        relevant = filter_relevant_results(request.query, tool_results)

        steps.append("Generating response")
        answer = await self._generate_answer(request.query, relevant)

        return ResearchResponse(
            query=request.query,
            steps=steps,
            tool_results=tool_results,
            answer=answer,
            confidence=calculate_confidence(tool_results),
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
        return calculate_confidence(results)
