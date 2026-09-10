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
    def __init__(self, api_key: str = None):
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

    async def plan_with_llm(self, query: str, client) -> Plan:
        try:
            tool_descriptions = "\n".join([
                f"- {t.value}: {self._tool_description(t)}" for t in ToolType
            ])
            system_prompt = f"""You are a research planner. Given a user query, select the most appropriate tools.

Available tools:
{tool_descriptions}

Respond with a JSON object containing:
- "tools": list of tool names to use (e.g., ["web_search", "calculator"])
- "reasoning": brief explanation of why these tools were selected"""

            response = await client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query},
                ],
                temperature=0,
            )

            import json
            content = response.choices[0].message.content
            result = json.loads(content)

            tools = []
            for tool_name in result.get("tools", []):
                try:
                    tool_type = ToolType(tool_name)
                    tools.append(ToolCall(tool=tool_type, parameters={"query": query}))
                except ValueError:
                    continue

            if not tools:
                tools = self._default_tool_selection(query)
                return Plan(
                    tools=tools,
                    reasoning="LLM selection returned no valid tools, using keyword fallback",
                )

            return Plan(
                tools=tools,
                reasoning=result.get("reasoning", "LLM-based tool selection"),
            )
        except Exception:
            tools = self._default_tool_selection(query)
            return Plan(
                tools=tools,
                reasoning="LLM planning failed, using keyword fallback",
            )

    def _tool_description(self, tool: ToolType) -> str:
        descriptions = {
            ToolType.WEB_SEARCH: "Search the web for information",
            ToolType.DATA_ANALYSIS: "Analyze CSV data and compute statistics",
            ToolType.CALCULATOR: "Perform mathematical calculations",
            ToolType.FILE_READER: "Read files, CSVs, and list directories",
        }
        return descriptions.get(tool, "Unknown tool")

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
