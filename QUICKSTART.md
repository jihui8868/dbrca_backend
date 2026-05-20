# Quick Start Guide

## Prerequisites

- Python 3.13+
- MySQL 5.7+ (with performance_schema enabled)
- OpenAI API key

## Installation

### 1. Clone and Setup Environment

```bash
cd /Users/jihui/code/db-rca/backend

# Create and activate virtual environment (if not using uv)
python3.13 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

### 3. Configure Environment

Create `.env` from template:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```bash
# MySQL connection
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=mysql

# OpenAI API
OPENAI_API_KEY=sk-your-api-key-here
LLM_MODEL=gpt-4
```

### 4. Enable Performance Schema (if needed)

```sql
-- Check if enabled
SHOW VARIABLES LIKE 'performance_schema';

-- If OFF, edit MySQL config and restart:
-- [mysqld]
-- performance_schema=ON
```

## Basic Usage

### CLI Mode

```bash
# Run diagnostic
python main.py
```

Output example:
```
Starting MySQL RCA Diagnostic System...

Testing database connection...
✓ Database connection successful

Diagnosing: Database queries are running slowly
--------------------------------------------------
========================================
MySQL RCA Diagnostic Report
========================================

Issue: Database queries are running slowly

Summary:
--------
Performance: warning
Logs: ok
Queries: warning
Configuration: ok

Analysis:
---------
[LLM-powered analysis results...]

Top Recommendations:
---------------------
1. Optimize identified slow queries
2. Defragment fragmented tables
3. Review index usage patterns
...
```

### Python Script

```python
from app.agents.root_cause_analyzer import RootCauseAnalyzer

# Initialize analyzer
analyzer = RootCauseAnalyzer()

# Run diagnostic
diagnosis = analyzer.diagnose("Database queries are slow")

# Get formatted report
report = analyzer.get_diagnostic_report("Database queries are slow")
print(report)

# Access findings directly
findings = analyzer._collect_findings()
print(f"Performance issues: {findings['performance']}")
```

### API Mode

```bash
# Start API server
python -m uvicorn app.api:app --reload --host 0.0.0.0 --port 8000
```

API endpoints:

```bash
# Health check
curl http://localhost:8000/health

# Run diagnostic
curl -X POST http://localhost:8000/api/v1/diagnostic/analyze \
  -H "Content-Type: application/json" \
  -d '{"issue_description": "Database is slow"}'

# Get metrics
curl http://localhost:8000/api/v1/diagnostic/metrics

# Get slow queries
curl http://localhost:8000/api/v1/diagnostic/slow-queries?limit=10

# Get full report
curl "http://localhost:8000/api/v1/diagnostic/report?issue=Database%20is%20slow"
```

## Diagnostic Output Structure

```python
{
    "status": "complete",
    "issue_description": "Database queries are slow",
    "findings_summary": {
        "performance_status": "warning",
        "log_status": "ok",
        "query_status": "warning",
        "config_status": "ok"
    },
    "recommendations": [
        "Optimize identified slow queries",
        "Defragment fragmented tables",
        "Remove unused indexes",
        ...
    ],
    "analysis": "LLM analysis results...",
    "detailed_findings": {
        "performance": {...},
        "logs": {...},
        "queries": {...},
        "configuration": {...}
    }
}
```

## Individual Sub-Agents

### Performance Analysis Only

```python
from app.agents.subagents import PerformanceAnalyzer

perf = PerformanceAnalyzer()
analysis = perf.analyze()

print(perf.get_summary())
# Output:
# Performance Analysis by Performance Analyzer:
# ⚠️  Found X slow queries
# 📊 Connection utilization: Y%
```

### Log Analysis Only

```python
from app.agents.subagents import LogAnalyzer

logs = LogAnalyzer()
analysis = logs.analyze()
print(logs.get_summary())
```

### Query Analysis Only

```python
from app.agents.subagents import QueryAnalyzer

queries = QueryAnalyzer()
analysis = queries.analyze()
print(queries.get_summary())
```

### Configuration Analysis Only

```python
from app.agents.subagents import ConfigInspector

config = ConfigInspector()
analysis = config.analyze()
print(config.get_summary())
```

## Database Management

### Test Connection

```python
from app.core.database import db_manager

if db_manager.test_connection():
    print("✓ Connected")
else:
    print("✗ Failed")
```

### Get Database Metrics

```python
from app.core.database import db_manager

# Slow queries
slow = db_manager.get_slow_queries(limit=10)

# Table statistics
stats = db_manager.get_table_statistics()

# Process list
processes = db_manager.get_process_list()

# Lock information
locks = db_manager.get_lock_info()

# Database size
size = db_manager.get_database_size()
```

## Configuration Reference

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| MYSQL_HOST | localhost | MySQL server host |
| MYSQL_PORT | 3306 | MySQL server port |
| MYSQL_USER | root | Database user |
| MYSQL_PASSWORD | (empty) | Database password |
| MYSQL_DATABASE | mysql | Target database |
| MYSQL_POOL_SIZE | 5 | Connection pool size |
| MYSQL_MAX_OVERFLOW | 10 | Max overflow connections |
| OPENAI_API_KEY | (required) | OpenAI API key |
| LLM_MODEL | gpt-4 | LLM model to use |
| LLM_TEMPERATURE | 0.7 | LLM temperature (0-1) |
| LLM_MAX_TOKENS | 2048 | Max tokens for LLM |
| AGENT_MAX_ITERATIONS | 10 | Max agent iterations |
| AGENT_TIMEOUT | 300 | Agent timeout (seconds) |
| AGENT_VERBOSE | false | Enable verbose logging |
| AGENT_DEBUG | false | Enable debug logging |

## Troubleshooting

### Connection Failed

```
Error: Database connection failed
```

**Solutions:**
- Check MYSQL_HOST and MYSQL_PORT
- Verify MySQL is running: `mysql -u root -p -e "SELECT 1"`
- Check credentials: `mysql -u MYSQL_USER -p MYSQL_PASSWORD`

### Performance Schema Not Available

```
Error: Failed to fetch slow queries
```

**Solutions:**
- Enable performance_schema in MySQL
- Restart MySQL: `systemctl restart mysql`
- Verify: `SHOW VARIABLES LIKE 'performance_schema';`

### OpenAI API Error

```
Error: Analysis failed: Invalid API key
```

**Solutions:**
- Check OPENAI_API_KEY is set
- Verify API key validity at https://platform.openai.com/account/api-keys
- Check API quota and usage

### Permission Denied

```
Error: Access denied for user
```

**Solutions:**
- Ensure database user has necessary permissions:
  ```sql
  GRANT SELECT ON *.* TO 'user'@'localhost';
  FLUSH PRIVILEGES;
  ```

## Next Steps

1. **Explore Sub-Agents**: Run individual sub-agents to understand their capabilities
2. **Customize Analysis**: Modify diagnostic prompts in root_cause_analyzer.py
3. **Add New Agents**: Create custom analyzers for specific needs
4. **API Integration**: Deploy as FastAPI service for your infrastructure
5. **Automate**: Schedule regular diagnostics with cron or your orchestration tool

## Example: Full Diagnostic Workflow

```python
from app.agents.root_cause_analyzer import RootCauseAnalyzer
from app.core.database import db_manager

# 1. Test connection
if not db_manager.test_connection():
    exit("Cannot connect to MySQL")

# 2. Initialize analyzer
analyzer = RootCauseAnalyzer()

# 3. Run diagnosis
issue = "Database has experienced recent performance degradation"
diagnosis = analyzer.diagnose(issue)

# 4. Process results
print(f"Status: {diagnosis['status']}")
print(f"\nFindings:")
for key, value in diagnosis['findings_summary'].items():
    print(f"  {key}: {value}")

print(f"\nTop 5 Recommendations:")
for i, rec in enumerate(diagnosis['recommendations'][:5], 1):
    print(f"  {i}. {rec}")

# 5. Get detailed report
report = analyzer.get_diagnostic_report(issue)
with open("diagnostic_report.txt", "w") as f:
    f.write(report)

print("\nReport saved to diagnostic_report.txt")
```

## Resources

- [README.md](README.md) - Full documentation
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Code organization
- [deepagents Documentation](https://github.com/agenthq/agents)
- [MySQL Performance Schema](https://dev.mysql.com/doc/refman/8.0/en/performance-schema.html)
- [OpenAI API Documentation](https://platform.openai.com/docs)
