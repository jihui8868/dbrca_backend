"""Example usage of the MySQL RCA system"""

from root_cause_analyzer import RootCauseAnalyzer
from subagents import (
    PerformanceAnalyzer,
    LogAnalyzer,
    QueryAnalyzer,
    ConfigInspector,
)


def example_individual_agents():
    """Example of using individual sub-agents"""
    print("=" * 60)
    print("Individual Agent Analysis Examples")
    print("=" * 60)

    # Performance Analyzer
    perf_analyzer = PerformanceAnalyzer()
    print("\n1. Performance Analysis:")
    print(perf_analyzer.get_summary())
    analysis = perf_analyzer.analyze()
    print(f"   Slow queries: {analysis['slow_queries'].get('count', 0)}")

    # Log Analyzer
    log_analyzer = LogAnalyzer()
    print("\n2. Log Analysis:")
    print(log_analyzer.get_summary())

    # Query Analyzer
    query_analyzer = QueryAnalyzer()
    print("\n3. Query Analysis:")
    print(query_analyzer.get_summary())

    # Configuration Inspector
    config_inspector = ConfigInspector()
    print("\n4. Configuration Analysis:")
    print(config_inspector.get_summary())


def example_orchestrated_diagnosis():
    """Example of using the orchestrated diagnosis"""
    print("\n" + "=" * 60)
    print("Orchestrated Diagnosis Examples")
    print("=" * 60)

    analyzer = RootCauseAnalyzer()

    # Example scenarios
    scenarios = [
        "Database queries are running very slowly",
        "High memory usage on MySQL server",
        "Connection timeouts occurring frequently",
        "General performance degradation",
    ]

    for scenario in scenarios[:1]:  # Run first scenario only
        print(f"\n📋 Scenario: {scenario}")
        print("-" * 60)

        try:
            report = analyzer.get_diagnostic_report(scenario)
            print(report)
        except Exception as e:
            print(f"Error: {e}")


def example_programmatic_access():
    """Example of programmatic access to diagnosis results"""
    print("\n" + "=" * 60)
    print("Programmatic Access Example")
    print("=" * 60)

    analyzer = RootCauseAnalyzer()

    diagnosis = analyzer.diagnose(
        issue_description="Database experiencing intermittent slowness"
    )

    print("\nDiagnosis Structure:")
    print(f"  Status: {diagnosis.get('status')}")
    print(f"  Issue: {diagnosis.get('issue_description')}")

    print("\nFindings Summary:")
    for key, value in diagnosis.get('findings_summary', {}).items():
        print(f"  {key}: {value}")

    print("\nTop Recommendations:")
    for i, rec in enumerate(diagnosis.get('recommendations', [])[:5], 1):
        print(f"  {i}. {rec}")

    print("\nDetailed Analysis:")
    analysis_text = diagnosis.get('analysis', '')
    if analysis_text:
        print(analysis_text[:500] + "...")


def example_custom_findings():
    """Example of accessing detailed findings"""
    print("\n" + "=" * 60)
    print("Detailed Findings Access")
    print("=" * 60)

    analyzer = RootCauseAnalyzer()
    findings = analyzer._collect_findings()

    print("\nPerformance Findings:")
    perf = findings.get('performance', {})
    if perf:
        print(f"  Status: {perf.get('slow_queries', {}).get('status')}")

    print("\nLog Analysis Findings:")
    logs = findings.get('logs', {})
    errors = logs.get('error_count', {})
    print(f"  Aborted connections: {errors.get('count', 0)}")

    print("\nQuery Analysis Findings:")
    queries = findings.get('queries', {})
    tables = queries.get('table_statistics', {})
    print(f"  Total tables: {tables.get('total_tables', 0)}")
    print(f"  Fragmented tables: {tables.get('fragmented_count', 0)}")


if __name__ == "__main__":
    # Run examples
    example_individual_agents()
    example_orchestrated_diagnosis()
    example_programmatic_access()
    example_custom_findings()

    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)
