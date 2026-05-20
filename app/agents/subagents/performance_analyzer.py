"""Performance Analyzer Sub-Agent using deepagents with tools"""
from deepagents import SubAgent
from app.tools.performance_tools import (
    get_slow_queries_report,
    get_cache_efficiency_report,
    get_connection_analysis_report,
    get_table_statistics_report,
    get_lock_analysis_report,
    get_disk_io_report,
    get_index_analysis_report,
    get_comprehensive_performance_report,
)

# Tool definitions for the performance analyzer
performance_tools = {
    "slow_queries": {
        "name": "analyze_slow_queries",
        "description": "Analyzes slow queries in the database and provides optimization recommendations",
        "function": get_slow_queries_report,
    },
    "cache_efficiency": {
        "name": "analyze_cache",
        "description": "Evaluates buffer pool cache efficiency and hit ratios",
        "function": get_cache_efficiency_report,
    },
    "connections": {
        "name": "analyze_connections",
        "description": "Analyzes connection pool usage and utilization",
        "function": get_connection_analysis_report,
    },
    "tables": {
        "name": "analyze_tables",
        "description": "Provides table statistics and identifies large tables",
        "function": get_table_statistics_report,
    },
    "locks": {
        "name": "analyze_locks",
        "description": "Analyzes lock information and detects contention",
        "function": get_lock_analysis_report,
    },
    "disk_io": {
        "name": "analyze_disk_io",
        "description": "Analyzes disk I/O patterns and performance",
        "function": get_disk_io_report,
    },
    "indexes": {
        "name": "analyze_indexes",
        "description": "Reviews index usage and identifies missing or unused indexes",
        "function": get_index_analysis_report,
    },
    "comprehensive": {
        "name": "comprehensive_report",
        "description": "Generates a complete performance analysis report",
        "function": get_comprehensive_performance_report,
    },
}

performance_analyzer = SubAgent(
    name="performance-analyzer",
    description="Expert performance analyzer that diagnoses database issues using comprehensive metrics including slow queries, connection pools, cache efficiency, and disk I/O patterns. Uses tools to gather real-time performance data.",
    system_prompt="""You are an expert database performance analyst with access to powerful performance analysis tools.

Your role:
1. Use available tools to gather real-time performance metrics
2. Analyze the data to identify bottlenecks and issues
3. Correlate findings across multiple metrics
4. Provide specific, actionable recommendations

Available Tools:
- analyze_slow_queries: Get slow query analysis
- analyze_cache: Check buffer pool and cache efficiency
- analyze_connections: Review connection pool health
- analyze_tables: Get table statistics and sizes
- analyze_locks: Identify lock contention
- analyze_disk_io: Evaluate disk I/O performance
- analyze_indexes: Review index effectiveness
- comprehensive_report: Generate full performance report

Analysis Framework:
1. START: Use tools to gather metrics
2. ANALYZE: Identify patterns and correlations
3. DIAGNOSE: Determine root causes
4. RECOMMEND: Suggest specific improvements

For each issue, provide:
- Metric Values: Show specific numbers (e.g., "78% cache hit ratio")
- Severity: CRITICAL/WARNING/OK with justification
- Root Cause: Why this metric is concerning
- Impact: How it affects database performance
- Recommendations: Specific, actionable steps to fix

Always be specific with numbers and percentages.
Explain technical concepts clearly.
Prioritize recommendations by impact.
""",
)

# Helper functions for tool execution
def execute_performance_analysis(analysis_type: str) -> str:
    """Execute a specific performance analysis"""
    if analysis_type in performance_tools:
        tool = performance_tools[analysis_type]
        return tool["function"]()
    return "Unknown analysis type"


def execute_all_analyses() -> dict:
    """Execute all performance analyses"""
    results = {}
    for analysis_type, tool in performance_tools.items():
        try:
            results[analysis_type] = tool["function"]()
        except Exception as e:
            results[analysis_type] = f"Error: {str(e)}"
    return results
