# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Multi-Database Root Cause Analysis (RCA) System** using the deepagents framework. Diagnoses database performance issues across MySQL, PostgreSQL, Informix, Oracle, SQL Server, and MariaDB by orchestrating four specialized sub-agents:

- **Performance Analyzer**: Query performance, cache efficiency, connections, disk I/O, indexes
- **Log Analyzer**: Error patterns, connection issues, warnings, replication status, log volume
- **Query Analyzer**: Query complexity, execution plans, JOIN patterns, subqueries, missing indexes
- **Config Inspector**: Configuration validation and optimization recommendations

All agents are LLM-agnostic: supports OpenAI, Deepseek, Anthropic, and Ollama (plus others via langchain).

---

## Architecture

### Core Components

**Entry Point** (`app/agents/main_agent.py`):
- `create_rca_agent()`: Creates the main orchestrator agent that coordinates all sub-agents
- `diagnose_database(issue_description)`: Main diagnostic function that invokes the RCA agent with a problem description

**Sub-Agents** (`app/agents/subagents/`):
- Each sub-agent is a deepagents `SubAgent` instance with specific tools and system prompts
- Tools live in `app/tools/` as modular, testable analysis functions returning `{"status", "message", "metrics", "recommendations"}`
- Each sub-agent follows an identical pattern: core class (e.g., `PerformanceMetrics`) + convenience functions

**Database Layer** (`app/core/database.py`):
- Universal `UniversalDatabaseManager` using SQLAlchemy + Strategy pattern
- Dialect abstraction in `database_types.py` handles database-specific SQL queries
- Supports MySQL, PostgreSQL, Informix, Oracle, SQL Server via configuration

**LLM Integration** (`app/core/llm_factory.py`):
- Factory pattern: `create_llm()` instantiates LangChain LLM based on config
- Provider-agnostic: OpenAI, Deepseek, Anthropic, Ollama, etc.
- API keys and models set via environment variables (see `.env.example`)

**Configuration** (`app/core/config.py`):
- Dataclass-based: `DatabaseConfig`, `LLMConfig`, `AgentConfig`
- Environment variable driven; supports both individual params and complete DSN
- Global `settings` instance used throughout

### Tool Implementation Pattern

All tools follow this template (see `app/tools/performance_tools.py`, `log_tools.py`, `query_tools.py`):

```python
class AnalyzerClass:
    @staticmethod
    def analyze_specific_aspect() -> Dict[str, Any]:
        return {
            "status": "OK|WARNING|CRITICAL|UNKNOWN",
            "message": "human-readable summary",
            "metrics": {...},
            "recommendations": ["actionable", "recommendations"]
        }
    
    @staticmethod
    def generate_report() -> Dict[str, Any]:
        # Aggregates all analyses, determines overall_status
        return {...}

def get_specific_aspect_report() -> str:
    # Convenience function for tool use; returns formatted string
    result = AnalyzerClass.analyze_specific_aspect()
    return f"Status: {result['status']}\n..."

tools = {
    "tool_key": {
        "name": "analyze_specific_aspect",
        "description": "...",
        "function": get_specific_aspect_report,
    }
}
```

---

## Environment & Configuration

### Setup

```bash
# 1. Create virtual environment (project uses Python 3.13+)
python3.13 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
uv pip install -e ".[all-llms,all-databases]"  # All LLM providers + database drivers
# OR install specific extras (see pyproject.toml)

# 3. Configure environment
cp .env.example .env
# Edit .env with your database and LLM credentials
```

### Key Environment Variables

**Database** (pick one approach):
- Approach 1: `DATABASE_TYPE`, `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`
- Approach 2: `DATABASE_URL` (complete DSN, overrides Approach 1)

**LLM**:
- `LLM_PROVIDER`: openai, deepseek, anthropic, ollama
- `LLM_MODEL`: format is "provider:model-name" or just "model-name"
- `OPENAI_API_KEY`, `DEEPSEEK_API_KEY`, `ANTHROPIC_API_KEY` (as needed)
- Optional: `DEEPSEEK_BASE_URL` (defaults to official API)

**Agent**:
- `AGENT_MAX_ITERATIONS=10`, `AGENT_TIMEOUT=300`, `AGENT_VERBOSE=false`, `AGENT_DEBUG=false`

---

## Common Development Tasks

### Run the Diagnostic System

```bash
# Basic diagnostic (uses main.py)
python main.py

# Diagnose a specific issue (python shell)
python -c "from app.agents.main_agent import diagnose_database; print(diagnose_database('Database queries are running slowly'))"

# Run all sub-agent analyses directly (for testing)
python -c "
from app.agents.subagents.performance_analyzer import execute_all_query_analyses
results = execute_all_query_analyses()
for analysis_type, result in results.items():
    print(f'{analysis_type}: {result}')
"
```

### Verify Setup

```bash
# Test imports and configuration
python test_setup.py

# Test database and LLM connections
python test_integration.py
```

### Add a New Analysis Tool

1. **Core implementation**: Add method to existing analyzer class (e.g., `PerformanceMetrics.analyze_new_metric()`)
2. **Convenience function**: Create `get_new_metric_report() -> str` wrapper
3. **Tool registration**: Add entry to `tools` dict with name, description, function
4. **Export**: Add to `app/tools/__init__.py` `__all__`
5. **Update sub-agent**: Add to `system_prompt` and `tools` dict in subagent file

### Run API Server

```bash
# Start FastAPI server (uses app/api.py and app/router/diagnostic.py)
uvicorn app.api:app --reload --host 0.0.0.0 --port 8000

# Then: curl http://localhost:8000/analyze_issue -X POST -d '{"issue": "..."}'
```

### Testing & Linting

```bash
# Run tests (pytest)
pytest

# Type checking
mypy app/

# Code formatting
black app/ --line-length 100

# Linting
flake8 app/ --max-line-length 100
```

---

## Project Structure

```
app/
├── agents/
│   ├── main_agent.py           # Main RCA orchestrator agent
│   ├── example_usage.py         # Usage examples
│   └── subagents/               # Specialized sub-agents
│       ├── performance_analyzer.py  # 7 tools for performance metrics
│       ├── log_analyzer.py          # 6 tools for log/event analysis
│       ├── query_analyzer.py        # 7 tools for query optimization
│       └── config_inspector.py      # Config validation (placeholder)
│
├── tools/                       # Analysis tool implementations
│   ├── performance_tools.py     # PerformanceMetrics class + 8 functions
│   ├── log_tools.py             # LogAnalyzer class + 7 functions
│   ├── query_tools.py           # QueryAnalyzer class + 8 functions
│   └── __init__.py              # Tool exports
│
├── core/
│   ├── config.py                # DatabaseConfig, LLMConfig, AgentConfig + settings
│   ├── database.py              # UniversalDatabaseManager (SQLAlchemy-based)
│   ├── database_types.py        # Strategy pattern for DB dialects
│   ├── llm_factory.py           # LLM provider factory (langchain)
│   └── __init__.py
│
├── router/
│   └── diagnostic.py            # FastAPI routes for HTTP API
│
└── api.py                       # FastAPI app setup and startup/shutdown

main.py                          # CLI entry point
test_setup.py                    # Import and config verification
test_integration.py              # Database and LLM connection tests
```

---

## Key Design Patterns & Decisions

### Synchronous Mode

All code uses synchronous functions (no `async/await`). This enables:
- Single-step debugging with breakpoints
- Simpler error handling in the multi-agent flow
- Easier integration with synchronous tools

### Unified Tool Output Format

All analysis tools return:
```python
{
    "status": "OK" | "WARNING" | "CRITICAL" | "UNKNOWN",
    "message": "summary (1-2 sentences)",
    "metrics": {...},              # tool-specific data
    "recommendations": [...]       # prioritized suggestions
}
```

This allows consistent handling by the main agent for synthesis and reporting.

### Multi-Database via Strategy Pattern

`database_types.py` maps each database type (MySQL, PostgreSQL, etc.) to a `DatabaseDialect` class that provides dialect-specific SQL queries. The `UniversalDatabaseManager` uses the detected DB type to pick the right dialect at runtime.

### Tool-Based Sub-Agents

Each sub-agent is a `deepagents.SubAgent` that:
1. Has a specialized system prompt describing its role and available tools
2. Registers tools via a `tools` dictionary (tool name → function)
3. Implements helper functions (`execute_<type>_analysis()`) for direct invocation

The main agent calls these sub-agents via deepagents' task orchestration, which handles LLM reasoning and tool invocation.

---

## Documentation

Comprehensive guides in the `doc/` directory (24 docs):
- **PERFORMANCE_TOOLS_GUIDE.md** – 7 performance analysis tools
- **LOG_TOOLS_GUIDE.md** – 6 log analysis tools  
- **QUERY_TOOLS_GUIDE.md** – 7 query analysis tools
- **MULTI_DATABASE_SUPPORT.md** – Multi-DB architecture and setup
- **LLM_INTEGRATION_SUMMARY.md** – LLM provider integration
- **DEBUG_GUIDE.md** – Debugging in VS Code, PyCharm, pdb
- **ARCHITECTURE.md** – System design and data flow
- **doc/INDEX.md** – Master index of all documentation

See `doc/INDEX.md` for guided reading paths by user type (developer, DBA, architect).

---

## Important Notes

1. **Database Connection**: The `db_manager` instance initializes on import. Set `DATABASE_TYPE`, `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` (or `DATABASE_URL`) before importing from `app.core.database`.

2. **LLM Selection**: `create_llm()` in `llm_factory.py` is the single point for instantiating LLMs. It handles provider detection and configuration validation.

3. **Sub-Agent Tooling**: When modifying sub-agents, update both the `system_prompt` (to inform the LLM of available tools) and the `tools` dict (to register functions the deepagents framework can invoke).

4. **Error Handling**: All tools have try-except blocks returning `{"status": "ERROR", "message": "..."}` on failure. The main agent synthesizes partial results gracefully.

5. **Extensibility**: To add a new analysis domain, create a new analyzer class in `app/tools/`, define its tools, create a new sub-agent in `app/agents/subagents/`, and update `main_agent.py` to include it in the orchestrator.
