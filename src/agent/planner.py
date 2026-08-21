from typing import Optional
from pydantic import BaseModel
from ..models.schemas import ToolType


class ToolCall(BaseModel):
    tool: ToolType
    parameters: dict


class Plan(BaseModel):
    tools: list[ToolCall]
    reasoning: str


class TaskPlanner:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    async def plan(
        self, query: str, preferred_tools: Optional[list[ToolType]] = None
    ) -> Plan:
        if preferred_tools:
            tools = [
                ToolCall(tool=tool, parameters={"query": query})
                for tool in preferred_tools
            ]
            return Plan(
                tools=tools,
                reasoning=f"Using preferred tools: {[t.value for t in preferred_tools]}",
            )

        tools = self._default_tool_selection(query)
        return Plan(
            tools=tools,
            reasoning="Auto-selected tools based on query analysis",
        )

    def _default_tool_selection(self, query: str) -> list[ToolCall]:
        query_lower = query.lower()
        tools = []

        if any(
            word in query_lower
            for word in ["search", "find", "look up", "web", "online"]
        ):
            tools.append(ToolCall(tool=ToolType.WEB_SEARCH, parameters={"query": query}))

        if any(
            word in query_lower
            for word in ["csv", "data", "analyze", "statistics", "numbers"]
        ):
            tools.append(
                ToolCall(tool=ToolType.DATA_ANALYSIS, parameters={"query": query})
            )

        if any(
            word in query_lower
            for word in ["calculate", "math", "compute", "sum", "average"]
        ):
            tools.append(
                ToolCall(tool=ToolType.CALCULATOR, parameters={"query": query})
            )

        if not tools:
            tools.append(ToolCall(tool=ToolType.WEB_SEARCH, parameters={"query": query}))

        return tools
