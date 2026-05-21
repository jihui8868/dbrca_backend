"""Log Analyzer Sub-Agent using deepagents with tools"""
from deepagents import SubAgent
from app.tools.log_tools import (
    get_error_patterns_report,
    get_connection_issues_report,
    get_warning_events_report,
    get_replication_status_report,
    get_log_volume_report,
    get_event_timeline_report,
    get_comprehensive_log_report,
)

# Tool definitions for the log analyzer
log_tools = {
    "error_patterns": {
        "name": "analyze_error_patterns",
        "description": "Analyzes error patterns from database logs and identifies common error types",
        "function": get_error_patterns_report,
    },
    "connection_issues": {
        "name": "analyze_connection_issues",
        "description": "Identifies connection-related errors and aborted connections",
        "function": get_connection_issues_report,
    },
    "warning_events": {
        "name": "analyze_warnings",
        "description": "Extracts and analyzes system warning events from logs",
        "function": get_warning_events_report,
    },
    "replication_status": {
        "name": "analyze_replication",
        "description": "Checks replication status and identifies replication-related issues",
        "function": get_replication_status_report,
    },
    "log_volume": {
        "name": "analyze_log_volume",
        "description": "Analyzes log volume and growth patterns",
        "function": get_log_volume_report,
    },
    "event_timeline": {
        "name": "analyze_event_timeline",
        "description": "Analyzes temporal patterns and event distribution in logs",
        "function": get_event_timeline_report,
    },
    "comprehensive": {
        "name": "comprehensive_log_report",
        "description": "Generates a complete log analysis report",
        "function": get_comprehensive_log_report,
    },
}

log_analyzer = SubAgent(
    name="log-analyzer",
    description="Expert log analyzer that diagnoses database issues by examining error logs, warnings, and diagnostic events. Uses tools to identify error patterns, connection issues, and replication problems.",
    system_prompt="""You are a MySQL diagnostics expert specializing in error logs and system events.

Your role:
1. Use available tools to gather log and event data
2. Analyze error patterns and connection issues
3. Identify replication and warning problems
4. Correlate findings across multiple log types
5. Provide specific, actionable recommendations

Available Tools:
- analyze_error_patterns: Get error pattern analysis
- analyze_connection_issues: Check connection-related problems
- analyze_warnings: Review system warning events
- analyze_replication: Check replication status
- analyze_log_volume: Evaluate log growth
- analyze_event_timeline: Analyze temporal patterns
- comprehensive_log_report: Generate full log analysis

Analysis Framework:
1. START: Use tools to gather logs and event data
2. ANALYZE: Identify patterns and correlations
3. DIAGNOSE: Determine root causes
4. RECOMMEND: Suggest specific improvements

For each issue, provide:
- Metric Values: Show specific numbers (e.g., "23 error events")
- Severity: CRITICAL/WARNING/OK with justification
- Root Cause: Why this pattern is concerning
- Impact: How it affects database operations
- Recommendations: Specific, actionable steps to resolve

Always be specific with error counts and patterns.
Explain error implications clearly.
Prioritize recommendations by severity and impact.
""",
)

# Helper functions for tool execution
def execute_log_analysis(analysis_type: str) -> str:
    """Execute a specific log analysis"""
    if analysis_type in log_tools:
        tool = log_tools[analysis_type]
        return tool["function"]()
    return "Unknown analysis type"


def execute_all_log_analyses() -> dict:
    """Execute all log analyses"""
    results = {}
    for analysis_type, tool in log_tools.items():
        try:
            results[analysis_type] = tool["function"]()
        except Exception as e:
            results[analysis_type] = f"Error: {str(e)}"
    return results
