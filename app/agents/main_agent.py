"""Main RCA Agent using deepagents - Orchestrator for Multi-Database Diagnosis"""
from deepagents import create_deep_agent
from app.agents.subagents import (
    performance_analyzer,
    log_analyzer,
    query_analyzer,
    config_inspector,
)
from app.core.config import settings
from app.core.database import db_manager
from app.core.llm_factory import create_llm


def create_rca_agent():
    """Create the main RCA agent with all sub-agents"""

    system_prompt = """You are the Multi-Database Root Cause Analysis (RCA) Expert. Your role is to diagnose database issues comprehensively across MySQL, PostgreSQL, Informix, and other databases.

You have access to four specialized sub-agents:
1. **performance-analyzer**: Analyzes performance metrics, slow queries, and resource usage
2. **log-analyzer**: Analyzes error logs, warnings, and diagnostic events
3. **query-analyzer**: Analyzes query patterns, optimization opportunities, and locking
4. **config-inspector**: Validates configuration and provides tuning recommendations

Your workflow when analyzing database issues:
1. FIRST: Ask the user or review the issue description
2. DELEGATE: Use the task() tool to call each sub-agent:
   - Call performance-analyzer to get performance metrics
   - Call log-analyzer to understand error patterns
   - Call query-analyzer to identify optimization opportunities
   - Call config-inspector to review configuration
3. SYNTHESIZE: Combine all findings into a comprehensive RCA:
   - Root cause identification
   - Severity assessment (CRITICAL/HIGH/MEDIUM/LOW)
   - Immediate action items
   - Long-term recommendations
4. PRESENT: Provide a structured diagnostic report

When calling sub-agents, provide them with:
- Specific questions about their domain
- Any database connection details or context
- Metrics or logs they should analyze

After receiving sub-agent responses:
- Cross-reference findings across sub-agents
- Identify patterns and correlations
- Weight the importance of each finding
- Provide integrated recommendations

Always structure your final analysis as:
## Root Cause Analysis Report

### Issue Summary
[Concise description of the issue]

### Severity: [CRITICAL/HIGH/MEDIUM/LOW]

### Findings by Domain
#### Performance Analysis
[Key performance findings]

#### Log & Event Analysis
[Error and warning patterns]

#### Query Analysis
[Query and optimization issues]

#### Configuration Analysis
[Configuration problems and improvements]

### Root Cause(s)
[Primary and secondary causes identified]

### Immediate Actions
1. [Action 1] - [Estimated time to impact]
2. [Action 2] - [Estimated time to impact]

### Long-Term Recommendations
1. [Optimization 1] - [Expected benefit]
2. [Optimization 2] - [Expected benefit]

### Monitoring Suggestions
[Metrics and alerts to track going forward]
"""

    # Create LLM using factory (supports OpenAI, Deepseek, Anthropic, Ollama, etc.)
    llm = create_llm(
        provider=settings.llm.provider,
        model=settings.llm.model,
        api_key=settings.llm.api_key,
    )

    agent = create_deep_agent(
        model=llm,  # Pass the LLM instance instead of model string
        system_prompt=system_prompt,
        subagents=[
            performance_analyzer,
            log_analyzer,
            query_analyzer,
            config_inspector,
        ],
    )

    return agent


def diagnose_database(issue_description: str):
    """
    Run a comprehensive database diagnosis

    Args:
        issue_description: Description of the database issue to diagnose

    Returns:
        Diagnostic analysis from the main RCA agent
    """
    agent = create_rca_agent()

    # Test database connection first
    if not db_manager.test_connection():
        return {
            "status": "error",
            "message": "Failed to connect to MySQL database. Please check your connection settings."
        }

    # Create diagnostic prompt with database info
    diagnostic_prompt = f"""Please perform a comprehensive MySQL Root Cause Analysis for the following issue:

Issue Description: {issue_description}

Please:
1. Use the task() tool to delegate to each sub-agent (performance-analyzer, log-analyzer, query-analyzer, config-inspector)
2. Gather comprehensive diagnostic data from the database
3. Synthesize all findings into a structured RCA report
4. Provide specific, actionable recommendations

Database: {db_manager.engine.url.database}
Host: {db_manager.engine.url.host}:{db_manager.engine.url.port}

Please begin the analysis.
"""

    # Invoke the agent with the diagnostic prompt
    try:
        result = agent.invoke({"messages": [{"role": "user", "content": diagnostic_prompt}]})
        return {
            "status": "success",
            "analysis": result,
            "issue_description": issue_description,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Analysis failed: {str(e)}"
        }
