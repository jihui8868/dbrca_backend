"""Query Analyzer Sub-Agent using deepagents with tools"""
from deepagents import SubAgent
from app.tools.query_tools import (
    get_query_complexity_report,
    get_execution_plans_report,
    get_join_patterns_report,
    get_subquery_efficiency_report,
    get_index_effectiveness_report,
    get_query_statistics_report,
    get_missing_indexes_report,
    get_comprehensive_query_report,
)

# Tool definitions for the query analyzer
query_tools = {
    "query_complexity": {
        "name": "analyze_query_complexity",
        "description": "Analyzes query complexity and identifies complex patterns that need optimization",
        "function": get_query_complexity_report,
    },
    "execution_plans": {
        "name": "analyze_execution_plans",
        "description": "Analyzes query execution plans and identifies inefficiencies",
        "function": get_execution_plans_report,
    },
    "join_patterns": {
        "name": "analyze_join_patterns",
        "description": "Analyzes JOIN patterns and identifies optimization opportunities",
        "function": get_join_patterns_report,
    },
    "subquery_efficiency": {
        "name": "analyze_subquery_efficiency",
        "description": "Analyzes subquery usage and efficiency issues",
        "function": get_subquery_efficiency_report,
    },
    "index_effectiveness": {
        "name": "analyze_index_effectiveness",
        "description": "Analyzes index usage and identifies unused or ineffective indexes",
        "function": get_index_effectiveness_report,
    },
    "query_statistics": {
        "name": "analyze_query_statistics",
        "description": "Analyzes query execution statistics and performance patterns",
        "function": get_query_statistics_report,
    },
    "missing_indexes": {
        "name": "identify_missing_indexes",
        "description": "Identifies missing indexes based on query patterns",
        "function": get_missing_indexes_report,
    },
    "comprehensive": {
        "name": "comprehensive_query_report",
        "description": "Generates a complete query analysis report",
        "function": get_comprehensive_query_report,
    },
}

query_analyzer = SubAgent(
    name="query-analyzer",
    description="Expert query analyzer that diagnoses query performance issues by examining complexity, execution plans, index usage, and JOIN patterns. Uses tools to identify optimization opportunities.",
    system_prompt="""You are a SQL query optimization expert with access to powerful query analysis tools.

Your role:
1. Use available tools to analyze query patterns and performance
2. Identify optimization bottlenecks in execution plans, JOINs, and subqueries
3. Evaluate index effectiveness and identify missing indexes
4. Correlate findings across multiple query metrics
5. Provide specific, actionable optimization recommendations

Available Tools:
- analyze_query_complexity: Get query complexity analysis
- analyze_execution_plans: Review execution plan efficiency
- analyze_join_patterns: Analyze JOIN optimization opportunities
- analyze_subquery_efficiency: Evaluate subquery performance
- analyze_index_effectiveness: Check index usage and effectiveness
- analyze_query_statistics: Get query performance statistics
- identify_missing_indexes: Find missing index opportunities
- comprehensive_query_report: Generate full query analysis

Analysis Framework:
1. START: Use tools to gather query and index metrics
2. ANALYZE: Identify patterns and correlations
3. DIAGNOSE: Determine optimization opportunities
4. RECOMMEND: Suggest specific improvements

For each issue, provide:
- Metric Values: Show specific numbers (e.g., "5 highly complex queries")
- Severity: CRITICAL/WARNING/OK with justification
- Root Cause: Why this is a performance issue
- Impact: How it affects query performance
- Recommendations: Specific, actionable optimization steps

Always be specific with query counts and execution times.
Explain optimization rationale clearly.
Prioritize recommendations by performance impact.
""",
)

# Helper functions for tool execution
def execute_query_analysis(analysis_type: str) -> str:
    """Execute a specific query analysis"""
    if analysis_type in query_tools:
        tool = query_tools[analysis_type]
        return tool["function"]()
    return "Unknown analysis type"


def execute_all_query_analyses() -> dict:
    """Execute all query analyses"""
    results = {}
    for analysis_type, tool in query_tools.items():
        try:
            results[analysis_type] = tool["function"]()
        except Exception as e:
            results[analysis_type] = f"Error: {str(e)}"
    return results
