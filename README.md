# MySQL RCA - Multi-Agent Root Cause Analysis System

A sophisticated multi-agent system for automated MySQL database diagnosis and root cause analysis using deepagents framework.

## Architecture

### Project Structure

```
app/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   └── database.py        # Database connection management
├── agents/
│   ├── __init__.py
│   ├── root_cause_analyzer.py    # Main orchestrator agent
│   └── subagents/
│       ├── __init__.py
│       ├── performance_analyzer.py    # Performance metrics analysis
│       ├── log_analyzer.py            # Error logs & patterns
│       ├── query_analyzer.py          # Query optimization analysis
│       └── config_inspector.py        # Configuration validation
└── [crud, models, router, schemas]    # Other application modules
```

## Components

### Core Modules

- **config.py**: Manages configuration for database, LLM, and agents
  - `DatabaseConfig`: MySQL connection settings
  - `LLMConfig`: OpenAI LLM configuration
  - `AgentConfig`: Multi-agent settings
  - `Settings`: Global settings instance

- **database.py**: Database connection management
  - `DatabaseManager`: Handles MySQL operations
  - Query execution, performance metrics collection
  - Lock and replication monitoring

### Sub-Agents

1. **Performance Analyzer**
   - Slow query detection
   - Connection pool analysis
   - Cache efficiency metrics
   - Disk I/O analysis

2. **Log Analyzer**
   - Error pattern detection
   - Connection failure analysis
   - Replication status monitoring
   - Warning event tracking

3. **Query Analyzer**
   - Slow query pattern analysis
   - Query optimization recommendations
   - Table statistics and fragmentation
   - Index usage analysis
   - Lock contention detection

4. **Configuration Inspector**
   - Memory settings validation
   - Connection configuration review
   - Logging configuration analysis
   - InnoDB settings optimization

### Main Orchestrator

**RootCauseAnalyzer**: Coordinates all sub-agents using deepagents framework
- Collects findings from all sub-agents
- Synthesizes analysis with LLM
- Provides prioritized recommendations
- Generates comprehensive diagnostic reports

## Setup

### Prerequisites

- Python 3.13+
- MySQL 5.7+ with performance_schema enabled
- OpenAI API key

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
# or with uv
uv sync
```

### Configuration

Set environment variables:

```bash
# Database
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
export MYSQL_USER=root
export MYSQL_PASSWORD=your_password
export MYSQL_DATABASE=mysql

# Database pool
export MYSQL_POOL_SIZE=5
export MYSQL_MAX_OVERFLOW=10

# LLM
export OPENAI_API_KEY=your_api_key
export LLM_MODEL=gpt-4
export LLM_TEMPERATURE=0.7
export LLM_MAX_TOKENS=2048

# Agents
export AGENT_MAX_ITERATIONS=10
export AGENT_TIMEOUT=300
export AGENT_VERBOSE=true
export AGENT_DEBUG=false
```

## Usage

### Running Diagnostics

```python
from app.agents.root_cause_analyzer import RootCauseAnalyzer

# Create analyzer
analyzer = RootCauseAnalyzer()

# Diagnose specific issue
report = analyzer.get_diagnostic_report("Database queries are running slowly")
print(report)
```

### Command Line

```bash
python main.py
```

### API Integration (FastAPI)

```python
from fastapi import FastAPI
from app.agents.root_cause_analyzer import RootCauseAnalyzer

app = FastAPI()
analyzer = RootCauseAnalyzer()

@app.post("/diagnose")
async def diagnose(issue: str):
    diagnosis = analyzer.diagnose(issue)
    return diagnosis

@app.get("/health")
async def health_check():
    from app.core.database import db_manager
    return {"connected": db_manager.test_connection()}
```

## Diagnostic Output

The system provides:

1. **Status Summary**
   - Performance status
   - Log analysis status
   - Query analysis status
   - Configuration status

2. **LLM Analysis**
   - Root cause assessment
   - Severity classification
   - Immediate actions

3. **Recommendations**
   - Query optimization tips
   - Configuration improvements
   - Index management suggestions
   - Memory tuning recommendations

## Performance Schema Requirements

Ensure MySQL performance schema is enabled:

```sql
-- Check if enabled
SHOW VARIABLES LIKE 'performance_schema';

-- Enable if needed (requires restart)
-- Add to my.cnf or my.ini
-- performance_schema=ON
```

## Features

- 🤖 Multi-agent orchestration using deepagents
- 📊 Real-time performance metrics collection
- 🔍 Intelligent query analysis and optimization
- ⚙️ Configuration validation and recommendations
- 📈 Lock contention and replication monitoring
- 🧠 LLM-powered root cause analysis
- 📋 Comprehensive diagnostic reports

## Extending the System

### Adding New Sub-Agents

1. Create new agent class in `app/agents/subagents/`
2. Implement analysis methods
3. Add to `RootCauseAnalyzer._collect_findings()`

### Custom Analysis

```python
class CustomAnalyzer:
    def __init__(self):
        self.name = "Custom Analyzer"
        
    def analyze(self):
        # Your analysis logic
        return findings
```

## Troubleshooting

### Database Connection Issues
- Verify MySQL is running
- Check credentials in environment variables
- Ensure user has appropriate permissions

### Performance Schema Not Available
- Check MySQL version (required for 5.7+)
- Verify performance_schema is enabled
- Restart MySQL after enabling

### LLM Analysis Failures
- Verify OPENAI_API_KEY is set
- Check API key validity
- Ensure sufficient API quota

## License

MIT
