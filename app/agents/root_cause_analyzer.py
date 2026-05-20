"""Root Cause Analyzer - Main orchestrator agent using deepagents"""
from typing import Dict, Any, List
from deepagents import SubAgent
from langchain_openai import ChatOpenAI

from .subagents import (
    PerformanceAnalyzer,
    LogAnalyzer,
    QueryAnalyzer,
    ConfigInspector,
)
from app.core.config import settings


class RootCauseAnalyzer:
    """Main multi-agent orchestrator for MySQL RCA"""

    def __init__(self):
        self.name = "Root Cause Analyzer"
        self.description = "Orchestrates sub-agents to diagnose MySQL database issues"

        # Initialize sub-agents
        self.performance_analyzer = PerformanceAnalyzer()
        self.log_analyzer = LogAnalyzer()
        self.query_analyzer = QueryAnalyzer()
        self.config_inspector = ConfigInspector()

        # Initialize LLM
        self.llm = ChatOpenAI(
            model=settings.llm.model,
            temperature=settings.llm.temperature,
            api_key=settings.llm.api_key,
        )

        # Initialize deepagents SubAgent
        self.subagent = SubAgent(
            name=self.name,
            description=self.description,
            model=settings.llm.model,
            verbose=settings.agent.verbose,
        )

    def diagnose(self, issue_description: str = "") -> Dict[str, Any]:
        """
        Perform comprehensive MySQL diagnosis

        Args:
            issue_description: Description of the issue to diagnose

        Returns:
            Dictionary containing diagnosis results and recommendations
        """
        # Collect data from all sub-agents
        findings = self._collect_findings()

        # Synthesize findings
        diagnosis = self._synthesize_diagnosis(findings, issue_description)

        return diagnosis

    def _collect_findings(self) -> Dict[str, Any]:
        """Collect findings from all sub-agents"""
        findings = {
            "performance": self.performance_analyzer.analyze(),
            "logs": self.log_analyzer.analyze(),
            "queries": self.query_analyzer.analyze(),
            "configuration": self.config_inspector.analyze(),
        }

        return findings

    def _synthesize_diagnosis(self, findings: Dict[str, Any], issue_description: str) -> Dict[str, Any]:
        """Synthesize findings into diagnosis and recommendations"""
        # Build context for LLM
        context = self._build_context(findings, issue_description)

        # Get LLM analysis
        analysis_prompt = f"""
Based on the following MySQL database analysis findings, provide:
1. Root cause analysis (what is likely causing the issue)
2. Severity assessment (critical/high/medium/low)
3. Immediate actions to take
4. Long-term optimization recommendations

Analysis findings:
{context}

Provide the response in a structured format.
"""

        # Use deepagents for analysis
        response = self._get_agent_analysis(analysis_prompt)

        return {
            "status": "complete",
            "issue_description": issue_description,
            "findings_summary": self._get_findings_summary(findings),
            "analysis": response,
            "detailed_findings": findings,
            "recommendations": self._extract_recommendations(findings),
        }

    def _build_context(self, findings: Dict[str, Any], issue_description: str) -> str:
        """Build context string from findings"""
        context = []

        if issue_description:
            context.append(f"Issue Description: {issue_description}\n")

        context.append("Performance Analysis:")
        context.append(f"  {self.performance_analyzer.get_summary()}\n")

        context.append("Log Analysis:")
        context.append(f"  {self.log_analyzer.get_summary()}\n")

        context.append("Query Analysis:")
        context.append(f"  {self.query_analyzer.get_summary()}\n")

        context.append("Configuration Analysis:")
        context.append(f"  {self.config_inspector.get_summary()}\n")

        return "\n".join(context)

    def _get_agent_analysis(self, prompt: str) -> str:
        """Get analysis from deepagents Agent"""
        try:
            # Use the LLM directly for analysis
            response = self.llm.invoke(prompt)
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            return f"Analysis error: {str(e)}"

    def _get_findings_summary(self, findings: Dict[str, Any]) -> Dict[str, str]:
        """Get summary of findings"""
        return {
            "performance_status": self._get_status(findings.get("performance", {})),
            "log_status": self._get_status(findings.get("logs", {})),
            "query_status": self._get_status(findings.get("queries", {})),
            "config_status": self._get_status(findings.get("configuration", {})),
        }

    @staticmethod
    def _get_status(analysis: Dict[str, Any]) -> str:
        """Extract status from analysis"""
        if "error" in analysis:
            return "error"

        # Check for warning status indicators
        slow_query_analysis = analysis.get("slow_query_analysis", {})
        if slow_query_analysis.get("status") == "warning":
            return "warning"

        analysis_status = analysis.get("status")
        if analysis_status in ["error", "warning", "ok"]:
            return analysis_status

        if analysis.get("lock_count"):
            return "warning"

        if analysis.get("count", 0) > 0:
            return "warning"

        return "ok"

    def _extract_recommendations(self, findings: Dict[str, Any]) -> List[str]:
        """Extract actionable recommendations"""
        recommendations = []

        # From performance analysis
        perf = findings.get("performance", {})
        slow_queries = perf.get("slow_query_analysis", {})
        if slow_queries.get("count", 0) > 0:
            recommendations.append("Optimize identified slow queries")

        # From query analysis
        query = findings.get("queries", {})
        query_analysis = query.get("slow_query_analysis", {})
        if query_analysis.get("count", 0) > 0:
            for q in query_analysis.get("queries", [])[:2]:
                if q.get("optimization_tips"):
                    recommendations.append(f"Apply optimization: {q['optimization_tips'][0]}")

        table_stats = query.get("table_statistics", {})
        if table_stats.get("fragmented_count", 0) > 0:
            recommendations.append(f"Defragment {table_stats['fragmented_count']} fragmented tables")

        if table_stats.get("unused_indexes_count", 0) > 0:
            recommendations.append(f"Remove {table_stats['unused_indexes_count']} unused indexes")

        # From configuration
        config = findings.get("configuration", {})
        memory = config.get("memory_settings", {})
        if memory.get("issues"):
            recommendations.append(f"Address memory issues: {memory['issues'][0]}")

        logging = config.get("logging_config", {})
        if logging.get("issues"):
            recommendations.append(f"Enable logging: {logging['issues'][0]}")

        # From logs
        logs = findings.get("logs", {})
        log_errors = logs.get("common_errors", {})
        if log_errors.get("count", 0) > 0:
            recommendations.append(f"Review {log_errors['count']} error patterns")

        return recommendations[:10]  # Limit to top 10 recommendations

    def get_diagnostic_report(self, issue_description: str = "") -> str:
        """Generate a formatted diagnostic report"""
        diagnosis = self.diagnose(issue_description)

        report = f"""
========================================
MySQL RCA Diagnostic Report
========================================

Issue: {diagnosis.get('issue_description', 'General diagnostic')}

Summary:
--------
Performance: {diagnosis['findings_summary'].get('performance_status', 'unknown')}
Logs: {diagnosis['findings_summary'].get('log_status', 'unknown')}
Queries: {diagnosis['findings_summary'].get('query_status', 'unknown')}
Configuration: {diagnosis['findings_summary'].get('config_status', 'unknown')}

Analysis:
---------
{diagnosis.get('analysis', 'No analysis available')}

Top Recommendations:
---------------------
"""

        for i, rec in enumerate(diagnosis.get('recommendations', []), 1):
            report += f"{i}. {rec}\n"

        report += "\n========================================\n"

        return report
