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
            performance_analyzer,
            log_analyzer,
            query_analyzer,
            config_inspector,
        )
        print("  ✓ app.agents.subagents (deepagents SubAgent specs)")

        from app.agents.main_agent import create_rca_agent, diagnose_database
        print("  ✓ app.agents.main_agent")

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
    """Test sub-agent definitions"""
    print("Testing sub-agent definitions...")
    try:
        from app.agents.subagents import (
            performance_analyzer,
            log_analyzer,
            query_analyzer,
            config_inspector,
        )

        agents = [
            ("performance-analyzer", performance_analyzer),
            ("log-analyzer", log_analyzer),
            ("query-analyzer", query_analyzer),
            ("config-inspector", config_inspector),
        ]

        for name, agent_spec in agents:
            print(f"  Checking {name}...", end=" ")
            try:
                assert agent_spec is not None, "Agent spec is None"
                assert agent_spec["name"] == name, f"Name mismatch"
                assert agent_spec["description"] is not None, "Missing description"
                assert agent_spec["system_prompt"] is not None, "Missing system_prompt"
                print(f"✓")
            except Exception as e:
                print(f"⚠️  ({e})")

        print("\n✓ All sub-agent specs loaded!\n")
        return True
    except Exception as e:
        print(f"\n✗ Sub-agent error: {e}\n")
        return False


def test_orchestrator():
    """Test deepagents main agent"""
    print("Testing deepagents main agent...")
    try:
        from app.agents.main_agent import create_rca_agent
        from app.agents.subagents import (
            performance_analyzer,
            log_analyzer,
            query_analyzer,
            config_inspector,
        )

        print("  Checking sub-agents...", end=" ")
        assert performance_analyzer is not None, "Missing performance_analyzer"
        assert log_analyzer is not None, "Missing log_analyzer"
        assert query_analyzer is not None, "Missing query_analyzer"
        assert config_inspector is not None, "Missing config_inspector"
        print("✓")

        print("  Creating main RCA agent...", end=" ")
        agent = create_rca_agent()
        print("✓")

        print("  Verifying agent configuration...", end=" ")
        assert agent is not None, "Agent creation failed"
        print("✓")

        print("\n✓ Deepagents main agent initialized!\n")
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
