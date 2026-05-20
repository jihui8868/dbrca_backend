"""Test script to verify MySQL RCA system setup"""
import sys
import os


def test_imports():
    """Test all imports work"""
    print("Testing imports...")
    try:
        from app.core.config import settings
        print("  ✓ app.core.config")

        from app.core.database import db_manager
        print("  ✓ app.core.database")

        from app.agents.subagents import (
            PerformanceAnalyzer,
            LogAnalyzer,
            QueryAnalyzer,
            ConfigInspector,
        )
        print("  ✓ app.agents.subagents")

        from app.agents.root_cause_analyzer import RootCauseAnalyzer
        print("  ✓ app.agents.root_cause_analyzer")

        print("\n✓ All imports successful!\n")
        return True
    except Exception as e:
        print(f"\n✗ Import error: {e}\n")
        return False


def test_config():
    """Test configuration"""
    print("Testing configuration...")
    try:
        from app.core.config import settings

        print(f"  Database Host: {settings.database.host}")
        print(f"  Database Port: {settings.database.port}")
        print(f"  Database User: {settings.database.user}")
        print(f"  LLM Model: {settings.llm.model}")
        print(f"  Agent Max Iterations: {settings.agent.max_iterations}")

        if not settings.llm.api_key:
            print("\n  ⚠️  Warning: OPENAI_API_KEY not set!")

        print("\n✓ Configuration loaded!\n")
        return True
    except Exception as e:
        print(f"\n✗ Config error: {e}\n")
        return False


def test_database():
    """Test database connection"""
    print("Testing database connection...")
    try:
        from app.core.database import db_manager

        if db_manager.test_connection():
            print("  ✓ Database connection successful!")

            try:
                size = db_manager.get_database_size()
                print(f"  Database info retrieved: {len(size)} database(s)")
            except Exception as e:
                print(f"  ⚠️  Could not retrieve database info: {e}")

            print("\n✓ Database test passed!\n")
            return True
        else:
            print("\n✗ Database connection failed!\n")
            print("  Please check MySQL connection settings:")
            print(f"    MYSQL_HOST: {os.getenv('MYSQL_HOST', 'localhost')}")
            print(f"    MYSQL_PORT: {os.getenv('MYSQL_PORT', '3306')}")
            print(f"    MYSQL_USER: {os.getenv('MYSQL_USER', 'root')}")
            print()
            return False
    except Exception as e:
        print(f"\n✗ Database error: {e}\n")
        return False


def test_sub_agents():
    """Test sub-agents"""
    print("Testing sub-agents...")
    try:
        from app.agents.subagents import (
            PerformanceAnalyzer,
            LogAnalyzer,
            QueryAnalyzer,
            ConfigInspector,
        )

        agents = [
            ("Performance Analyzer", PerformanceAnalyzer()),
            ("Log Analyzer", LogAnalyzer()),
            ("Query Analyzer", QueryAnalyzer()),
            ("Configuration Inspector", ConfigInspector()),
        ]

        for name, agent in agents:
            print(f"  Testing {name}...", end=" ")
            try:
                # Get summary (won't run full analysis if no data)
                summary = agent.get_summary()
                print(f"✓")
            except Exception as e:
                print(f"⚠️  ({e})")

        print("\n✓ Sub-agents loaded!\n")
        return True
    except Exception as e:
        print(f"\n✗ Sub-agent error: {e}\n")
        return False


def test_orchestrator():
    """Test orchestrator"""
    print("Testing orchestrator...")
    try:
        from app.agents.root_cause_analyzer import RootCauseAnalyzer

        print("  Initializing RootCauseAnalyzer...", end=" ")
        analyzer = RootCauseAnalyzer()
        print("✓")

        print("  Checking sub-agents...", end=" ")
        assert hasattr(analyzer, 'performance_analyzer'), "Missing performance_analyzer"
        assert hasattr(analyzer, 'log_analyzer'), "Missing log_analyzer"
        assert hasattr(analyzer, 'query_analyzer'), "Missing query_analyzer"
        assert hasattr(analyzer, 'config_inspector'), "Missing config_inspector"
        assert hasattr(analyzer, 'llm'), "Missing LLM"
        assert hasattr(analyzer, 'subagent'), "Missing deepagents SubAgent"
        print("✓")

        print("\n✓ Orchestrator initialized!\n")
        return True
    except Exception as e:
        print(f"\n✗ Orchestrator error: {e}\n")
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("MySQL RCA System Setup Verification")
    print("=" * 60 + "\n")

    tests = [
        test_imports,
        test_config,
        test_sub_agents,
        test_orchestrator,
        test_database,
    ]

    results = []
    for test in tests:
        results.append(test())
        print()

    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")

    if all(results):
        print("\n✓ System is ready to use!")
        print("\nNext steps:")
        print("  1. Set OPENAI_API_KEY environment variable")
        print("  2. Run: python main.py")
        print("  3. Or start API: python -m uvicorn app.api:app --reload")
        print("\nFor more info, see QUICKSTART.md")
        return 0
    else:
        print("\n✗ Some tests failed. Check errors above.")
        print("\nFor help, see QUICKSTART.md - Troubleshooting section")
        return 1


if __name__ == "__main__":
    sys.exit(main())
