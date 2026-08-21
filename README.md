# AI Research Agent

An AI agent that processes research queries through **tool calling** and **structured analysis**. Demonstrates practical agent architecture with web search, data analysis, and file processing tools.

## Why I Built This

This project demonstrates my understanding of **agentic AI systems** — moving beyond simple LLM chatbots to build agents that can plan, use tools, validate results, and generate structured responses.

## Architecture

```
User Query
    ↓
Intent Detection
    ↓
Task Planning
    ↓
Tool Selection
    ↓
Tool Execution
    ↓
Result Validation
    ↓
Structured Response
```

## Features

- **Tool-calling architecture** with dynamic tool selection
- **Structured outputs** using Pydantic models
- **Multiple tools**: web search, data analysis, file processing, calculator
- **FastAPI REST API** for inference
- **Docker containerization** for deployment
- **Comprehensive logging** and error handling

## Tech Stack

- Python 3.10+
- FastAPI
- OpenAI / LLM APIs
- Pydantic
- Docker

## Project Structure

```
ai-research-agent/
├── src/
│   ├── agent/
│   │   ├── core.py          # Agent orchestrator
│   │   ├── planner.py       # Task planning
│   │   └── executor.py      # Tool execution
│   ├── tools/
│   │   ├── web_search.py    # Web search tool
│   │   ├── data_analysis.py # CSV/data analysis
│   │   └── calculator.py    # Math operations
│   ├── models/
│   │   └── schemas.py       # Pydantic models
│   ├── api/
│   │   └── app.py           # FastAPI endpoints
│   └── utils/
│       └── config.py        # Settings management
├── tests/
├── examples/
├── docs/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

## Installation

```bash
git clone https://github.com/Abelastro/ai-research-agent.git
cd ai-research-agent
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

## Configuration

```bash
cp .env.example .env
# Edit .env with your API keys
```

## Usage

### API Server

```bash
python -m src.main
# or
uvicorn src.api.app:app --reload
```

### Example Request

```python
import requests

response = requests.post("http://localhost:8000/research", json={
    "query": "Analyze the CSV data in sales.csv and summarize key trends",
    "tools": ["data_analysis", "calculator"]
})
print(response.json())
```

## How It Works

1. **User submits a research query**
2. **Planner** decomposes the query into sub-tasks
3. **Tool selector** determines which tools are needed
4. **Executor** runs each tool with proper parameters
5. **Validator** checks results for completeness
6. **Responder** generates a structured final answer

## Limitations

- Prototype/experimental system
- Requires API key for LLM access
- Tool results are not cached between sessions

## Future Improvements

- Add streaming responses
- Implement tool result caching
- Add more specialized tools
- Build evaluation suite
