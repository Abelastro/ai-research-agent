# Architecture

## Overview

The AI Research Agent follows a modular architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────┐
│                  FastAPI Server                   │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌─────────────┐    ┌─────────────┐             │
│  │   Planner   │───▶│   Executor  │             │
│  └─────────────┘    └─────────────┘             │
│         │                    │                   │
│         ▼                    ▼                   │
│  ┌─────────────┐    ┌─────────────┐             │
│  │   Tools     │    │   Models    │             │
│  └─────────────┘    └─────────────┘             │
│                                                  │
└─────────────────────────────────────────────────┘
```

## Components

### Agent Core
Orchestrates the research workflow: planning → execution → validation → response.

### Task Planner
Analyzes user queries and determines which tools to use.

### Tool Executor
Runs selected tools and collects results.

### Tools
- **Web Search**: Search the web for information
- **Data Analysis**: Analyze CSV data
- **Calculator**: Perform calculations

### API Layer
FastAPI endpoints for external integration.
