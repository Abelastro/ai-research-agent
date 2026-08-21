from pydantic import BaseModel
from typing import Optional
from enum import Enum


class ToolType(str, Enum):
    WEB_SEARCH = "web_search"
    DATA_ANALYSIS = "data_analysis"
    CALCULATOR = "calculator"
    FILE_READER = "file_reader"


class ResearchRequest(BaseModel):
    query: str
    tools: Optional[list[ToolType]] = None


class ToolResult(BaseModel):
    tool: ToolType
    input: dict
    output: str
    success: bool
    error: Optional[str] = None


class ResearchResponse(BaseModel):
    query: str
    steps: list[str]
    tool_results: list[ToolResult]
    answer: str
    confidence: float
