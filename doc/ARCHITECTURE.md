# MySQL RCA - Architecture Documentation

## System Overview

The MySQL RCA (Root Cause Analysis) system is a sophisticated multi-agent application that diagnoses MySQL database issues using a coordinated team of specialized agents powered by the deepagents framework.

```
┌─────────────────────────────────────────────────────────────┐
│                   Root Cause Analyzer                        │
│            (Main Orchestrator using deepagents)              │
└─────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
        ┌───────┴─────┐  ┌────┴────┐  ┌────┴────┐
        │ Performance │  │   Log   │  │  Query  │
        │ Analyzer    │  │ Analyzer│  │ Analyzer│
        └─────────────┘  └─────────┘  └─────────┘
                │
        ┌───────┴───────┐
        │ Configuration │
        │  Inspector    │
        └───────────────┘
```

## Component Architecture

### 1. Core Module (`app/core/`)

#### config.py
Configuration management using dataclasses and environment variables.

**Components:**
- `DatabaseConfig`: MySQL connection parameters
- `LLMConfig`: OpenAI LLM settings
- `AgentConfig`: Multi-agent framework settings
- `Settings`: Global configuration singleton

**Key Features:**
- Environment variable fallbacks
- Automatic type conversion
- Connection string generation

#### database.py
Database abstraction layer for MySQL operations.

**Components:**
- `DatabaseManager`: Main connection manager
- Connection pooling with SQLAlchemy
- Query execution interface
- Performance metrics collection

**Key Methods:**
- `get_session()`: Get database session
- `execute_query()`: Run SELECT queries
- `execute_command()`: Run INSERT/UPDATE/DELETE
- `get_slow_queries()`: Retrieve slow query metrics
- `get_process_list()`: Current connections
- `get_lock_info()`: Lock contention data
- `get_table_statistics()`: Storage and fragmentation

### 2. Agents Module (`app/agents/`)

#### Sub-Agents Structure

Each sub-agent is a specialized analyzer focusing on one aspect:

```
SubAgent Interface:
├── __init__()
│   ├── name: str
│   └── description: str
├── analyze() -> Dict[str, Any]
├── get_summary() -> str
└── [specific analysis methods]
```

#### PerformanceAnalyzer

Analyzes performance metrics and bottlenecks.

**Analysis Areas:**
1. **Slow Queries**
   - Query digest analysis
   - Execution count and timing
   - Performance degradation indicators

2. **Connection Pool**
   - Active connection count
   - Utilization percentage
   - Connection configuration

3. **Cache Efficiency**
   - Buffer pool hit ratio
   - Cache effectiveness metrics

4. **Disk I/O**
   - Top I/O consuming tables
   - Read/write patterns

**Output:**
```python
{
    "slow_queries": {...},
    "connection_info": {...},
    "cache_efficiency": {...},
    "disk_io": {...}
}
```

#### LogAnalyzer

Analyzes error patterns and diagnostic events.

**Analysis Areas:**
1. **Error Count**
   - Aborted connections
   - Connection issues severity

2. **Common Errors**
   - Top error types
   - Error frequency patterns

3. **Warnings**
   - System variable alerts
   - Critical condition detection

4. **Replication Status**
   - Slave thread health
   - Replication lag

**Output:**
```python
{
    "error_count": {...},
    "common_errors": {...},
    "warning_events": {...},
    "replication_status": {...}
}
```

#### QueryAnalyzer

Analyzes query execution patterns and optimization opportunities.

**Analysis Areas:**
1. **Slow Query Patterns**
   - Query categorization
   - Optimization recommendations

2. **Table Statistics**
   - Large tables
   - Fragmented tables
   - Space usage

3. **Index Usage**
   - Used vs unused indexes
   - Index efficiency metrics

4. **Lock Analysis**
   - Lock contention detection
   - Blocking query identification

**Output:**
```python
{
    "slow_query_analysis": {...},
    "table_statistics": {...},
    "index_usage": {...},
    "lock_analysis": {...}
}
```

#### ConfigInspector

Validates MySQL configuration and identifies optimization opportunities.

**Analysis Areas:**
1. **Memory Settings**
   - Buffer pool size
   - Sort buffer configuration
   - Cache settings

2. **Connection Settings**
   - Max connections
   - Packet size limits
   - Timeout values

3. **Logging Configuration**
   - Slow query log status
   - Error logging
   - Replication logging

4. **InnoDB Settings**
   - Flush mode
   - Log file size
   - Lock mode

**Output:**
```python
{
    "memory_settings": {...},
    "connection_settings": {...},
    "logging_config": {...},
    "innodb_settings": {...}
}
```

#### RootCauseAnalyzer

Main orchestrator agent that coordinates all sub-agents.

**Architecture:**
1. **Collection Phase**
   - Invokes all sub-agents in parallel
   - Collects findings from each

2. **Synthesis Phase**
   - Builds context from findings
   - Sends to LLM for analysis
   - Receives interpretation

3. **Recommendation Phase**
   - Extracts actionable recommendations
   - Prioritizes by severity
   - Generates diagnostic report

**Key Methods:**
```python
def diagnose(issue_description: str) -> Dict[str, Any]
def _collect_findings() -> Dict[str, Any]
def _synthesize_diagnosis(findings, issue) -> Dict[str, Any]
def get_diagnostic_report(issue: str) -> str
```

### 3. API Module (`app/api.py` and `app/router/diagnostic.py`)

FastAPI application exposing the multi-agent system as REST endpoints.

**Endpoints:**

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | System health check |
| POST | `/api/v1/diagnostic/analyze` | Run diagnostic analysis |
| GET | `/api/v1/diagnostic/report` | Get detailed report |
| GET | `/api/v1/diagnostic/metrics` | Get performance metrics |
| GET | `/api/v1/diagnostic/slow-queries` | List slow queries |
| GET | `/api/v1/diagnostic/table-stats` | Get table statistics |
| GET | `/api/v1/diagnostic/lock-info` | Get lock information |
| GET | `/api/v1/diagnostic/process-list` | Get process list |

## Data Flow

### Diagnostic Request Flow

```
User Request
    │
    ↓
RootCauseAnalyzer.diagnose()
    │
    ├─→ PerformanceAnalyzer.analyze()
    │   └─→ DatabaseManager queries
    │
    ├─→ LogAnalyzer.analyze()
    │   └─→ DatabaseManager queries
    │
    ├─→ QueryAnalyzer.analyze()
    │   └─→ DatabaseManager queries
    │
    └─→ ConfigInspector.analyze()
        └─→ DatabaseManager queries
    │
    ↓
Findings Aggregation
    │
    ↓
LLM Synthesis
(ChatOpenAI)
    │
    ↓
Recommendation Extraction
    │
    ↓
Diagnostic Report
```

## Integration with deepagents

The RootCauseAnalyzer uses deepagents for LLM-powered analysis:

```python
from deepagents import Agent
from langchain_openai import ChatOpenAI

class RootCauseAnalyzer:
    def __init__(self):
        self.llm = ChatOpenAI(...)
        self.agent = Agent(
            name="Root Cause Analyzer",
            llm=self.llm,
            max_iterations=10,
            verbose=True
        )
```

**Key Features:**
- Automatic tool use for analysis
- Iterative reasoning
- Error recovery
- Configurable iterations

## Configuration Hierarchy

```
Environment Variables (highest priority)
    ↓
DatabaseConfig/LLMConfig/AgentConfig
    ↓
Settings singleton
    ↓
Default values (lowest priority)
```

## Error Handling

- Database connection failures → Graceful degradation
- Missing performance schema → Feature skipping
- LLM API errors → Fallback to data-only analysis
- Query failures → Logged with explanation

## Performance Considerations

1. **Query Caching**: Reuse query results within diagnostic window
2. **Connection Pooling**: SQLAlchemy QueuePool for efficient connections
3. **Async Ready**: FastAPI integration for concurrent requests
4. **Agent Iterations**: Configurable max iterations to limit runtime

## Extensibility

### Adding New Sub-Agents

1. Create new analyzer class in `subagents/`
2. Implement `analyze()` method
3. Register in `RootCauseAnalyzer._collect_findings()`
4. Update report generation logic

### Custom LLM Models

Replace ChatOpenAI with any langchain-compatible LLM:
```python
self.llm = YourCustomLLM(...)
```

### Database Backends

DatabaseManager abstracts SQL operations, can support other databases by extending interface.

## Security Considerations

1. **Credentials**: Use environment variables, never hardcode
2. **API Access**: Add authentication middleware as needed
3. **Query Isolation**: All database operations use parameterized queries
4. **Error Messages**: Sanitize sensitive information in API responses

## Monitoring and Logging

System supports configurable logging:
- `AGENT_VERBOSE=true`: Agent operation logging
- `AGENT_DEBUG=true`: SQLAlchemy query logging
- API logs via FastAPI

## Future Enhancements

1. Persistent storage of diagnostic results
2. Trending analysis over time
3. Automated remediation suggestions
4. Integration with alerting systems
5. Custom agent templates
6. Web UI dashboard
7. Multi-database support
8. Machine learning for pattern detection
