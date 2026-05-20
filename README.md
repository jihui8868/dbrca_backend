# Multi-Database RCA - Multi-Agent Root Cause Analysis System

A sophisticated multi-agent system for automated database diagnosis and root cause analysis using deepagents framework.

**支持的数据库:** MySQL, PostgreSQL, Informix, MariaDB, Oracle, SQL Server  
**支持的 LLM:** OpenAI, Deepseek, Anthropic Claude, Ollama  
**框架:** deepagents + FastAPI

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

Set environment variables. See [doc/同步模式改造完成报告.md](./doc/同步模式改造完成报告.md) for detailed setup.

#### Database Configuration
```bash
# Method 1: Individual parameters
export DATABASE_TYPE=mysql                    # mysql, postgresql, informix, etc.
export DB_HOST=localhost
export DB_PORT=3306
export DB_USER=root
export DB_PASSWORD=your_password
export DB_NAME=testdb

# Method 2: Complete DSN
export DATABASE_URL=mysql+pymysql://root:password@localhost:3306/testdb
```

#### LLM Configuration
```bash
# Provider selection
export LLM_PROVIDER=openai                    # openai, deepseek, anthropic, ollama
export LLM_MODEL=openai:gpt-4                 # format: provider:model-name

# API Keys (choose based on provider)
export OPENAI_API_KEY=sk-xxx...               # For OpenAI
export DEEPSEEK_API_KEY=sk-xxx...             # For Deepseek
export ANTHROPIC_API_KEY=sk-ant-xxx...        # For Anthropic
# Ollama: no API key needed

# Model parameters
export LLM_TEMPERATURE=0.7
export LLM_MAX_TOKENS=2048
export LLM_TIMEOUT=30
export LLM_MAX_RETRIES=3
```

#### Agent Configuration
```bash
export AGENT_MAX_ITERATIONS=10
export AGENT_TIMEOUT=300
export AGENT_VERBOSE=true
export AGENT_DEBUG=false
```

### Installation Options
```bash
# Basic install (OpenAI + MySQL)
pip install -e .

# With Anthropic support
pip install -e .[anthropic]

# With all LLM providers
pip install -e .[all-llms]

# With all database drivers
pip install -e .[all-databases]

# Complete setup
pip install -e .[all]
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
- 🧠 LLM-powered root cause analysis (Multiple providers)
- 📋 Comprehensive diagnostic reports
- 💾 Multi-database support (MySQL, PostgreSQL, Informix, etc.)
- 🎯 Multiple LLM providers (OpenAI, Deepseek, Anthropic, Ollama)
- 🐍 Synchronous mode for easy debugging

## 📚 Documentation

All documentation is located in the `doc/` directory. Quick links:

### Getting Started
- [Sync Mode Report (中文)](./doc/同步模式改造完成报告.md) - Quick start guide
- [Quick Start LLM](./doc/QUICK_START_LLM.md) - Setup LLM providers
- [Quick Start](./doc/QUICKSTART.md) - Initial setup

### Debugging
- [Debug Guide](./doc/DEBUG_GUIDE.md) - Complete debugging guide
- [Sync Mode Migration](./doc/SYNC_MODE_MIGRATION.md) - Synchronous mode details

### Multi-Database
- [Multi-Database Support](./doc/MULTI_DATABASE_SUPPORT.md) - Database configuration
- [Multi-Database Checklist](./doc/MULTI_DATABASE_CHECKLIST.md) - Verification

### Multi-LLM
- [LLM Integration Summary](./doc/LLM_INTEGRATION_SUMMARY.md) - Technical details
- [Usage Examples](./doc/USAGE_EXAMPLES.md) - Real-world scenarios

### Architecture
- [Architecture](./doc/ARCHITECTURE.md) - System design
- [Project Structure](./doc/PROJECT_STRUCTURE.md) - File organization

### Complete Index
📖 **See [doc/INDEX.md](./doc/INDEX.md) for complete documentation index**

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
