# Project Structure

```
backend/
├── app/                                    # Main application package
│   ├── __init__.py
│   ├── api.py                             # FastAPI application
│   │
│   ├── core/                              # Core modules
│   │   ├── __init__.py
│   │   ├── config.py                      # Configuration management
│   │   │   ├── DatabaseConfig             # MySQL configuration
│   │   │   ├── LLMConfig                  # OpenAI LLM settings
│   │   │   ├── AgentConfig                # Multi-agent settings
│   │   │   └── Settings                   # Global settings
│   │   │
│   │   └── database.py                    # Database connection management
│   │       ├── DatabaseManager            # Connection & query management
│   │       │   ├── get_session()
│   │       │   ├── execute_query()
│   │       │   ├── execute_command()
│   │       │   ├── get_slow_queries()
│   │       │   ├── get_table_statistics()
│   │       │   ├── get_process_list()
│   │       │   └── get_lock_info()
│   │       │
│   │       └── db_manager                 # Global database manager instance
│   │
│   ├── agents/                            # Multi-agent system
│   │   ├── __init__.py
│   │   ├── root_cause_analyzer.py         # Main orchestrator agent
│   │   │   ├── RootCauseAnalyzer         # Main class using deepagents
│   │   │   │   ├── diagnose()            # Run comprehensive diagnosis
│   │   │   │   ├── _collect_findings()   # Gather from sub-agents
│   │   │   │   ├── _synthesize_diagnosis()  # Analyze with LLM
│   │   │   │   └── get_diagnostic_report()  # Generate report
│   │   │   │
│   │   │   └── [integration with deepagents.Agent]
│   │   │
│   │   ├── example_usage.py               # Usage examples
│   │   │
│   │   └── subagents/                     # Specialized sub-agents
│   │       ├── __init__.py
│   │       ├── performance_analyzer.py    # Performance metrics analysis
│   │       │   ├── PerformanceAnalyzer
│   │       │   │   ├── analyze()
│   │       │   │   ├── _get_slow_queries()
│   │       │   │   ├── _get_connection_info()
│   │       │   │   ├── _get_cache_efficiency()
│   │       │   │   ├── _get_disk_io_info()
│   │       │   │   └── get_summary()
│   │       │
│   │       ├── log_analyzer.py            # Error logs & patterns
│   │       │   ├── LogAnalyzer
│   │       │   │   ├── analyze()
│   │       │   │   ├── _get_error_count()
│   │       │   │   ├── _get_common_errors()
│   │       │   │   ├── _get_warnings()
│   │       │   │   ├── _get_replication_status()
│   │       │   │   └── get_summary()
│   │       │
│   │       ├── query_analyzer.py          # Query optimization
│   │       │   ├── QueryAnalyzer
│   │       │   │   ├── analyze()
│   │       │   │   ├── _analyze_slow_queries()
│   │       │   │   ├── _get_table_statistics()
│   │       │   │   ├── _analyze_index_usage()
│   │       │   │   ├── _analyze_locks()
│   │       │   │   └── get_summary()
│   │       │
│   │       └── config_inspector.py        # Configuration validation
│   │           ├── ConfigInspector
│   │           │   ├── analyze()
│   │           │   ├── _check_memory_settings()
│   │           │   ├── _check_connection_settings()
│   │           │   ├── _check_logging_config()
│   │           │   ├── _check_innodb_settings()
│   │           │   └── get_summary()
│   │
│   ├── router/                            # API endpoints
│   │   ├── __init__.py
│   │   └── diagnostic.py                  # Diagnostic API routes
│   │       ├── /health                    # Health check
│   │       ├── /api/v1/diagnostic/analyze # Run diagnostic
│   │       ├── /api/v1/diagnostic/report  # Get report
│   │       ├── /api/v1/diagnostic/metrics # Performance metrics
│   │       ├── /api/v1/diagnostic/slow-queries
│   │       ├── /api/v1/diagnostic/table-stats
│   │       ├── /api/v1/diagnostic/lock-info
│   │       └── /api/v1/diagnostic/process-list
│   │
│   ├── crud/                              # CRUD operations (placeholder)
│   ├── models/                            # SQLAlchemy models (placeholder)
│   ├── schemas/                           # Pydantic schemas (placeholder)
│   └── [other modules as needed]
│
├── main.py                                # CLI entry point
├── pyproject.toml                         # Project dependencies
├── uv.lock                                # Lock file (uv)
│
├── README.md                              # User documentation
├── ARCHITECTURE.md                        # System architecture
├── PROJECT_STRUCTURE.md                   # This file
├── .env.example                           # Environment variables template
├── .gitignore                             # Git ignore rules
├── .python-version                        # Python version (3.13)
│
└── .git/                                  # Git repository
```

## File Descriptions

### Core Files

| File | Purpose |
|------|---------|
| `main.py` | CLI entry point for diagnostics |
| `app/api.py` | FastAPI application factory |
| `pyproject.toml` | Project metadata and dependencies |

### Core Module (`app/core/`)

| File | Purpose |
|------|---------|
| `config.py` | Configuration management with environment variables |
| `database.py` | MySQL connection pooling and query execution |

### Agents Module (`app/agents/`)

| File | Purpose |
|------|---------|
| `root_cause_analyzer.py` | Main orchestrator using deepagents framework |
| `example_usage.py` | Usage examples and testing |
| `subagents/performance_analyzer.py` | Performance metrics analysis |
| `subagents/log_analyzer.py` | Error and log pattern analysis |
| `subagents/query_analyzer.py` | Query optimization recommendations |
| `subagents/config_inspector.py` | Configuration validation |

### API Module (`app/router/`)

| File | Purpose |
|------|---------|
| `diagnostic.py` | RESTful API endpoints for diagnostics |

### Other Directories

| Directory | Purpose |
|-----------|---------|
| `crud/` | Database CRUD operations (expandable) |
| `models/` | SQLAlchemy ORM models |
| `schemas/` | Pydantic request/response schemas |

## Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                       │
│                       (app/api.py)                           │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ↓
        ┌──────────────────────┐
        │ API Routes           │
        │ (router/diagnostic)  │
        └──────┬───────────────┘
               │
               ↓
    ┌──────────────────────────────┐
    │ Root Cause Analyzer          │
    │ (Main Orchestrator Agent)    │
    │ Using deepagents.Agent       │
    └──────┬───────────────────────┘
           │
    ┌──────┴──────┬───────────┬───────────┐
    ↓             ↓           ↓           ↓
┌────────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│Performance │ │Log       │ │Query     │ │Config    │
│Analyzer    │ │Analyzer  │ │Analyzer  │ │Inspector │
└─────┬──────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘
      │             │            │            │
      └─────────────┴────────────┴────────────┘
                     │
                     ↓
        ┌─────────────────────────┐
        │ Database Manager        │
        │ (core/database.py)      │
        │ SQLAlchemy Pool         │
        └────────────┬────────────┘
                     │
                     ↓
            ┌─────────────────────┐
            │   MySQL Server      │
            │ Performance Schema  │
            │ Information Schema  │
            └─────────────────────┘
```

## Module Relationships

```
main.py
└── RootCauseAnalyzer
    ├── DatabaseManager
    │   └── MySQL Connection Pool
    ├── PerformanceAnalyzer
    │   └── DatabaseManager
    ├── LogAnalyzer
    │   └── DatabaseManager
    ├── QueryAnalyzer
    │   └── DatabaseManager
    ├── ConfigInspector
    │   └── DatabaseManager
    └── ChatOpenAI (via deepagents.Agent)
        └── LLM Analysis

app/api.py (FastAPI)
├── router/diagnostic.py
│   └── RootCauseAnalyzer
└── Middleware (CORS, etc.)

config.py
├── DatabaseConfig
├── LLMConfig
├── AgentConfig
└── Settings (Singleton)
```

## Configuration Flow

```
Environment Variables
    ↓
config.py (DatabaseConfig, LLMConfig, AgentConfig)
    ↓
Settings singleton
    ↓
DatabaseManager / RootCauseAnalyzer initialization
    ↓
Runtime execution
```

## Sub-Agent Analysis Flow

Each sub-agent follows this pattern:

```
analyze() [main entry point]
    ├── _method1()  [specific analysis]
    ├── _method2()  [specific analysis]
    ├── _method3()  [specific analysis]
    └── _method4()  [specific analysis]
        │
        ↓
    Returns: Dict[str, Any]
        │
        ├── status: "ok" | "warning" | "error"
        ├── findings: [analysis results]
        └── recommendations: [actionable items]
        
get_summary() [formatted output]
    └── Returns: str (human-readable summary)
```

## Extension Points

### Adding New Sub-Agents
Create file: `app/agents/subagents/new_analyzer.py`
```python
class NewAnalyzer:
    def __init__(self):
        self.name = "..."
        self.description = "..."
    
    def analyze(self):
        # Implementation
        return {...}
    
    def get_summary(self):
        # Implementation
        return "..."
```

### Adding New API Endpoints
Add to: `app/router/diagnostic.py`
```python
@router.get("/new-endpoint")
async def new_endpoint():
    # Implementation
    return {...}
```

### Adding New Database Queries
Extend: `app/core/database.py`
```python
def get_custom_data(self):
    query = "SELECT ..."
    return self.execute_query(query)
```

## Dependencies

- **deepagents**: Multi-agent orchestration
- **langchain-openai**: LLM integration
- **fastapi**: Web API framework
- **sqlalchemy**: ORM and database abstraction
- **pymysql**: MySQL driver
- **pydantic**: Data validation
- **uvicorn**: ASGI server

See `pyproject.toml` for versions.
