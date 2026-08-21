from ..models.schemas import ToolResult, ToolType
from .planner import ToolCall
from ..tools.web_search import web_search
from ..tools.data_analysis import data_analysis
from ..tools.calculator import calculator


class ToolExecutor:
    def __init__(self):
        self.tool_map = {
            ToolType.WEB_SEARCH: web_search,
            ToolType.DATA_ANALYSIS: data_analysis,
            ToolType.CALCULATOR: calculator,
        }

    async def execute(self, tool_call: ToolCall) -> ToolResult:
        tool_func = self.tool_map.get(tool_call.tool)

        if not tool_func:
            return ToolResult(
                tool=tool_call.tool,
                input=tool_call.parameters,
                output="",
                success=False,
                error=f"Tool {tool_call.tool.value} not implemented",
            )

        try:
            output = await tool_func(**tool_call.parameters)
            return ToolResult(
                tool=tool_call.tool,
                input=tool_call.parameters,
                output=output,
                success=True,
            )
        except Exception as e:
            return ToolResult(
                tool=tool_call.tool,
                input=tool_call.parameters,
                output="",
                success=False,
                error=str(e),
            )
