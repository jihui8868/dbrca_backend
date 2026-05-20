"""Main application entry point for MySQL RCA"""
import asyncio
from app.agents.root_cause_analyzer import RootCauseAnalyzer
from app.core.database import db_manager


async def main():
    """Run MySQL RCA diagnostic"""
    print("Starting MySQL RCA Diagnostic System...\n")

    # Test database connection
    print("Testing database connection...")
    if not db_manager.test_connection():
        print("❌ Failed to connect to MySQL database")
        print("Please configure MYSQL_* environment variables")
        return

    print("✓ Database connection successful\n")

    # Initialize Root Cause Analyzer
    analyzer = RootCauseAnalyzer()

    # Example issue descriptions to diagnose
    issue_descriptions = [
        "Database queries are running slowly",
        "High memory usage detected",
        "Connection timeout errors occurring",
    ]

    # Run diagnostic for each issue
    for issue in issue_descriptions[:1]:  # Run first issue as example
        print(f"Diagnosing: {issue}")
        print("-" * 50)

        try:
            report = analyzer.get_diagnostic_report(issue)
            print(report)
        except Exception as e:
            print(f"Error during diagnosis: {e}")
            import traceback
            traceback.print_exc()

    print("\nDiagnostic complete!")


if __name__ == "__main__":
    asyncio.run(main())
