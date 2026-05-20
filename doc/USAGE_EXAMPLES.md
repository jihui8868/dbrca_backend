# Usage Examples: Multi-Provider & Multi-Database

Complete examples showing how to use the RCA system with different LLM providers and databases.

## Example 1: OpenAI + MySQL (Production Setup)

Most reliable combination for production environments.

### Setup

```bash
# 1. Install dependencies
pip install -e .  # Default includes OpenAI

# 2. Configure environment
cat > .env << 'EOF'
# Database
DATABASE_TYPE=mysql
DB_HOST=production-mysql.example.com
DB_PORT=3306
DB_USER=root
DB_PASSWORD=secure_password
DB_NAME=production_db

# LLM
LLM_PROVIDER=openai
LLM_MODEL=openai:gpt-4
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxx
LLM_TEMPERATURE=0.3  # Lower temperature for consistent analysis
LLM_MAX_TOKENS=2048
EOF

# 3. Run diagnostic
python main.py
```

### Output Example

```
Starting MySQL RCA Diagnostic System (deepagents Multi-Agent)

Testing database connection...
✓ Database connection successful

Diagnosing: Database queries are running slowly
============================================================
🤖 Initializing OPENAI LLM: gpt-4

## Root Cause Analysis Report

### Issue Summary
Database queries are experiencing significantly degraded performance with response times exceeding expected baselines.

### Severity: HIGH

### Findings by Domain
#### Performance Analysis
- Query execution time: 2.5s average (baseline: 200ms)
- Missing indexes on frequently queried columns
- Table scan operations on large tables

#### Log & Event Analysis
- Lock contention detected in InnoDB
- Connection pool exhaustion warnings
- Slow query log shows 500+ queries > 1s

#### Query Analysis
- Full table scan on 10M row table
- Non-optimized JOIN operations
- Missing composite indexes

#### Configuration Analysis
- max_connections too low (150 vs recommended 500)
- query_cache_size deprecated setting still enabled
- innodb_buffer_pool_size only 1GB (recommend 8GB+)

### Root Cause(s)
1. PRIMARY: Missing indexes on frequently accessed columns
2. SECONDARY: Insufficient database configuration (memory allocation)
3. TERTIARY: Connection pool saturation

### Immediate Actions
1. Add composite index on (user_id, created_date) - 5min
2. Increase max_connections to 500 - 2min
3. Increase innodb_buffer_pool_size to 8GB - 10min (requires restart)

### Long-Term Recommendations
1. Query optimization review - Save 60-80% execution time
2. Partitioning strategy for large tables - Improve maintenance
3. ReadReplica setup - Enable horizontal scaling

### Monitoring Suggestions
Track: Query response time, Lock wait time, Connection pool utilization
====================================================================
Diagnostic complete!
```

## Example 2: Deepseek + PostgreSQL (Cost-Efficient Staging)

Balance between cost and performance for staging/testing.

### Setup

```bash
# 1. Install with Deepseek support
pip install -e .  # Already includes OpenAI-compatible base for Deepseek

# 2. Configure environment
export LLM_PROVIDER=deepseek
export LLM_MODEL=deepseek:deepseek-chat
export DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxx

export DATABASE_TYPE=postgresql
export DB_HOST=staging-postgres.example.com
export DB_PORT=5432
export DB_USER=postgres
export DB_PASSWORD=staging_password
export DB_NAME=staging_db

# 3. Run diagnostic
python main.py
```

### Cost Comparison

```
Single diagnostic with Deepseek vs OpenAI:
- Deepseek:  ~$0.001 (99.9% cheaper)
- OpenAI:    ~$0.12

For 1000 diagnostics per month:
- Deepseek:  ~$1.00
- OpenAI:    ~$120.00
```

### Python Code Example

```python
import os
from app.agents.main_agent import diagnose_database

# Switch to Deepseek programmatically
os.environ['LLM_PROVIDER'] = 'deepseek'
os.environ['LLM_MODEL'] = 'deepseek:deepseek-chat'
os.environ['DEEPSEEK_API_KEY'] = 'sk-xxx...'
os.environ['DATABASE_TYPE'] = 'postgresql'

# Run diagnosis (cost ~$0.001)
result = diagnose_database("Database replication is lagging")

if result['status'] == 'success':
    print(result['analysis'])
```

## Example 3: Anthropic Claude + Informix (Advanced Analysis)

For complex reasoning and advanced database analysis.

### Setup

```bash
# 1. Install with Anthropic support
pip install -e .[anthropic]

# 2. Configure environment
export LLM_PROVIDER=anthropic
export LLM_MODEL=anthropic:claude-opus-4
export ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxx

export DATABASE_TYPE=informix
export DB_HOST=legacy-informix.example.com
export DB_PORT=9088
export DB_USER=informix
export DB_PASSWORD=informix_password
export DB_NAME=legacy_db

# 3. Run diagnostic
python main.py
```

### Advanced Analysis Example

```python
from app.agents.main_agent import diagnose_database

# Complex issue requiring advanced reasoning
issue = """
We have intermittent application timeouts that appear to be related to database 
performance, but only on weekdays during business hours (9am-5pm). The issue 
doesn't occur on weekends or after 5pm. Query logs show normal execution times 
in the slow query log, but the application reports 30-60 second timeouts. 
This suggests the issue might be related to connection pooling, lock contention, 
or network latency rather than pure query performance.
"""

# Use Claude's advanced reasoning
result = diagnose_database(issue)

if result['status'] == 'success':
    # Claude will provide deeper analysis including:
    # - Connection pool configuration issues
    # - Lock contention patterns during business hours
    # - Network topology considerations
    # - Correlation with business activities
    print(result['analysis'])
```

## Example 4: Ollama + Multiple Databases (Development)

Local development with zero API costs - test different databases.

### Setup

```bash
# 1. Start Ollama (in separate terminal)
ollama serve

# 2. Pull a model
ollama pull mistral

# 3. Configure for MySQL
export LLM_PROVIDER=ollama
export LLM_MODEL=ollama:mistral
export DATABASE_TYPE=mysql
export DB_HOST=localhost
export DB_PORT=3306

# 4. Run diagnostic
python main.py

# 5. Later, switch to PostgreSQL without stopping Ollama
export DATABASE_TYPE=postgresql
export DB_PORT=5432

# 6. Run again with same LLM
python main.py
```

### Development Workflow

```python
#!/usr/bin/env python3
"""
Development workflow: Test diagnostics with different databases
using the same local LLM (Ollama) to save costs
"""

import os
from app.agents.main_agent import diagnose_database

# Use local Ollama for all tests (free)
os.environ['LLM_PROVIDER'] = 'ollama'
os.environ['LLM_MODEL'] = 'ollama:mistral'

test_configs = [
    {
        'name': 'MySQL',
        'env': {
            'DATABASE_TYPE': 'mysql',
            'DB_HOST': 'localhost',
            'DB_PORT': '3306',
        }
    },
    {
        'name': 'PostgreSQL',
        'env': {
            'DATABASE_TYPE': 'postgresql',
            'DB_HOST': 'localhost',
            'DB_PORT': '5432',
        }
    },
    {
        'name': 'Informix',
        'env': {
            'DATABASE_TYPE': 'informix',
            'DB_HOST': 'localhost',
            'DB_PORT': '9088',
        }
    }
]

issue = "Database responding slowly to SELECT queries"

for config in test_configs:
    print(f"\nTesting with {config['name']}...")
    
    # Update environment
    for key, value in config['env'].items():
        os.environ[key] = value
    
    # Run diagnosis (free with Ollama)
    result = diagnose_database(issue)
    
    if result['status'] == 'success':
        print(f"✓ {config['name']} analysis complete")
    else:
        print(f"✗ {config['name']} analysis failed: {result['message']}")
```

## Example 5: Multi-Database Analysis (Enterprise)

Analyze multiple databases in a single run using different providers.

### Setup & Execution

```python
#!/usr/bin/env python3
"""
Enterprise scenario: Diagnose multiple databases across different cloud providers
"""

from app.core.database import UniversalDatabaseManager
from app.core.llm_factory import create_llm

# Define databases to analyze
databases = {
    'Production MySQL': {
        'dsn': 'mysql+pymysql://root:pwd@prod-mysql.aws.com:3306/maindb',
        'llm_provider': 'openai',  # Production-grade analysis
        'llm_model': 'gpt-4',
    },
    'Staging PostgreSQL': {
        'dsn': 'postgresql+psycopg2://postgres:pwd@staging-pg.azure.com:5432/testdb',
        'llm_provider': 'deepseek',  # Cost-effective for staging
        'llm_model': 'deepseek-chat',
    },
    'Legacy Informix': {
        'dsn': 'informix+pyodbc://informix:pwd@legacy.datacenter.com:9088/legacydb',
        'llm_provider': 'anthropic',  # Advanced reasoning for legacy
        'llm_model': 'claude-opus-4',
    }
}

issue = "Database response times degraded after maintenance window"

for db_name, config in databases.items():
    print(f"\n{'='*60}")
    print(f"Analyzing: {db_name}")
    print('='*60)
    
    # Create database manager
    db = UniversalDatabaseManager(config['dsn'])
    
    # Create LLM with provider-specific key
    if config['llm_provider'] == 'openai':
        api_key = os.getenv('OPENAI_API_KEY')
    elif config['llm_provider'] == 'deepseek':
        api_key = os.getenv('DEEPSEEK_API_KEY')
    elif config['llm_provider'] == 'anthropic':
        api_key = os.getenv('ANTHROPIC_API_KEY')
    
    llm = create_llm(
        provider=config['llm_provider'],
        model=config['llm_model'],
        api_key=api_key
    )
    
    # Get database information
    print(f"Database Type: {db.db_type.name}")
    print(f"Dialect: {type(db.dialect).__name__}")
    print(f"LLM Provider: {config['llm_provider']}")
    
    # Test connection
    if db.test_connection():
        print("Connection: ✓ Success")
        
        # Perform analysis
        # (Would call agent here with database-specific context)
    else:
        print("Connection: ✗ Failed")
```

## Example 6: Programmatic Usage (API)

Integrate into your application using the REST API.

```python
# main_api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.agents.main_agent import diagnose_database

app = FastAPI()

class DiagnosticRequest(BaseModel):
    issue_description: str
    llm_provider: str = "openai"  # Optional override
    database_type: str = "mysql"  # Optional override

@app.post("/api/diagnose")
async def diagnose(request: DiagnosticRequest):
    """Run database diagnostic"""
    try:
        result = diagnose_database(request.issue_description)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

```bash
# Usage
curl -X POST http://localhost:8000/api/diagnose \
  -H "Content-Type: application/json" \
  -d '{"issue_description": "Slow query performance"}'
```

## Example 7: Cost Optimization

Tier different analysis by importance and cost.

```python
#!/usr/bin/env python3
"""
Cost-optimized diagnostic strategy:
- CRITICAL issues: Use GPT-4 (high cost, best accuracy)
- HIGH issues: Use Deepseek (low cost, good accuracy)
- MEDIUM issues: Use Claude Sonnet (medium cost)
- LOW issues: Use Ollama (free, local)
"""

import os
from app.agents.main_agent import diagnose_database
from app.core.config import settings

SEVERITY_TO_PROVIDER = {
    'CRITICAL': ('openai', 'gpt-4'),
    'HIGH': ('deepseek', 'deepseek-chat'),
    'MEDIUM': ('anthropic', 'claude-sonnet'),
    'LOW': ('ollama', 'llama2'),
}

def analyze_with_appropriate_provider(issue: str, severity: str):
    """Select LLM provider based on issue severity"""
    
    provider, model = SEVERITY_TO_PROVIDER.get(severity, ('deepseek', 'deepseek-chat'))
    
    # Set provider
    os.environ['LLM_PROVIDER'] = provider
    os.environ['LLM_MODEL'] = f'{provider}:{model}'
    
    # Set API key based on provider
    if provider == 'openai':
        os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
    elif provider == 'deepseek':
        os.environ['DEEPSEEK_API_KEY'] = os.getenv('DEEPSEEK_API_KEY')
    elif provider == 'anthropic':
        os.environ['ANTHROPIC_API_KEY'] = os.getenv('ANTHROPIC_API_KEY')
    # Ollama needs no API key
    
    print(f"Analyzing {severity} issue with {provider} ({model})")
    result = diagnose_database(issue)
    
    return result

# Examples
critical = "Production database is completely down"
high = "Database connections being dropped"
medium = "Slow query performance"
low = "Advisory: Update statistics"

analyze_with_appropriate_provider(critical, 'CRITICAL')  # Uses GPT-4
analyze_with_appropriate_provider(high, 'HIGH')          # Uses Deepseek
analyze_with_appropriate_provider(medium, 'MEDIUM')      # Uses Claude
analyze_with_appropriate_provider(low, 'LOW')            # Uses Ollama
```

## Summary

These examples demonstrate the flexibility of the system:

1. **Production:** OpenAI + MySQL for reliability
2. **Staging:** Deepseek + PostgreSQL for cost efficiency
3. **Enterprise:** Different providers for different databases
4. **Development:** Ollama locally, no costs
5. **Complex:** Anthropic for advanced reasoning
6. **API:** Integration into existing applications
7. **Optimization:** Cost-based provider selection

The system requires **zero code changes** to switch between these configurations!
