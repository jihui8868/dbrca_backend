"""Main application entry point for MySQL RCA using deepagents"""
import asyncio
from app.agents.main_agent import diagnose_database
from app.core.database import db_manager


async def main():
    """Run MySQL RCA diagnostic using deepagents"""
    print("Starting MySQL RCA Diagnostic System (deepagents Multi-Agent)\n")

    # Test database connection
    print("Testing database connection...")
    if not db_manager.test_connection():
        print("❌ Failed to connect to MySQL database")
        print("Please configure MYSQL_* environment variables")
        return

    print("✓ Database connection successful\n")

    # Example issue descriptions to diagnose
    issue_descriptions = [
        "Database queries are running slowly",
    ]

    # Run diagnostic for each issue
    for issue in issue_descriptions:
        print(f"Diagnosing: {issue}")
        print("=" * 60)

        try:
            result = diagnose_database(issue)

            if result["status"] == "success":
                print(result.get("analysis", ""))
            else:
                print(f"Error: {result['message']}")

        except Exception as e:
            print(f"Error during diagnosis: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 60)
    print("Diagnostic complete!")


if __name__ == "__main__":
    asyncio.run(main())
