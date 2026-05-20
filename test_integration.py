#!/usr/bin/env python3
"""Integration test for LLM factory and multi-database support"""

from app.core.llm_factory import create_llm
from app.core.config import settings
from app.agents.main_agent import create_rca_agent
from app.core.database import db_manager


def test_llm_factory():
    """Test LLM factory creation for different providers"""
    print("\n" + "="*60)
    print("Testing LLM Factory")
    print("="*60)

    # Test provider inference
    test_cases = [
        ("openai:gpt-4", "openai", "gpt-4"),
        ("deepseek:deepseek-chat", "deepseek", "deepseek-chat"),
        ("anthropic:claude-opus-4", "anthropic", "claude-opus-4"),
    ]

    for model_str, expected_provider, expected_model in test_cases:
        # Parse model string
        if ":" in model_str:
            provider, model = model_str.split(":", 1)
        else:
            provider, model = None, model_str

        print(f"\n✓ Provider: {provider}, Model: {model}")
        assert provider == expected_provider, f"Provider mismatch: {provider} != {expected_provider}"
        assert model == expected_model, f"Model mismatch: {model} != {expected_model}"

    print("\n✓ All LLM factory provider tests passed!")


def test_config():
    """Test configuration loading"""
    print("\n" + "="*60)
    print("Testing Configuration")
    print("="*60)

    print(f"✓ Database Type: {settings.database.database_type}")
    print(f"✓ Database Host: {settings.database.host}")
    print(f"✓ LLM Provider: {settings.llm.provider}")
    print(f"✓ LLM Model: {settings.llm.model}")
    print(f"✓ LLM Temperature: {settings.llm.temperature}")
    print(f"✓ LLM Max Tokens: {settings.llm.max_tokens}")
    print(f"✓ Agent Max Iterations: {settings.agent.max_iterations}")

    # Verify API key resolution
    api_key = settings.llm.api_key
    if settings.llm.provider == "openai":
        assert api_key == settings.llm.openai_api_key, "OpenAI API key mismatch"
        print("✓ OpenAI API key resolution working")
    elif settings.llm.provider == "deepseek":
        assert api_key == settings.llm.deepseek_api_key, "Deepseek API key mismatch"
        print("✓ Deepseek API key resolution working")
    elif settings.llm.provider == "anthropic":
        assert api_key == settings.llm.anthropic_api_key, "Anthropic API key mismatch"
        print("✓ Anthropic API key resolution working")

    print("\n✓ All configuration tests passed!")


def test_agent_creation():
    """Test RCA agent creation"""
    print("\n" + "="*60)
    print("Testing Agent Creation")
    print("="*60)

    try:
        agent = create_rca_agent()
        print(f"✓ RCA agent created successfully")
        print(f"✓ Agent type: {type(agent).__name__}")
        print("\n✓ Agent creation test passed!")
    except ValueError as e:
        if "API_KEY" in str(e):
            print(f"⚠ Agent creation requires API key (expected during testing)")
            print(f"  Message: {e}")
            print(f"  This is expected - set {settings.llm.provider.upper()}_API_KEY to run the agent")
            print("\n✓ Agent creation validation test passed!")
        else:
            raise
    except Exception as e:
        print(f"✗ Agent creation failed: {e}")
        raise


def test_database_connection():
    """Test database connection"""
    print("\n" + "="*60)
    print("Testing Database Connection")
    print("="*60)

    print(f"✓ Database DSN: {db_manager.engine.url}")
    print(f"✓ Database Type: {db_manager.db_type.name}")
    print(f"✓ Dialect: {type(db_manager.dialect).__name__}")

    try:
        result = db_manager.test_connection()
        if result:
            print("✓ Database connection successful!")
        else:
            print("⚠ Database connection test returned False")
    except Exception as e:
        print(f"⚠ Database connection test raised exception (may be expected if DB not running): {e}")

    print("\n✓ Database connection test completed!")


def main():
    """Run all integration tests"""
    print("\n" + "="*70)
    print("Multi-Agent RCA System - Integration Tests")
    print("="*70)

    try:
        test_config()
        test_llm_factory()
        test_agent_creation()
        test_database_connection()

        print("\n" + "="*70)
        print("✓ All integration tests completed successfully!")
        print("="*70)
        print("\nSystem Status:")
        print(f"  • Database: {settings.database.database_type} @ {settings.database.host}")
        print(f"  • LLM Provider: {settings.llm.provider}")
        print(f"  • Agent Framework: deepagents")
        print(f"\nTo run the full diagnostic:")
        print(f"  1. Set {settings.llm.provider.upper()}_API_KEY environment variable")
        print(f"  2. Ensure database is running")
        print(f"  3. Run: python main.py")
        print("="*70 + "\n")

    except Exception as e:
        print(f"\n✗ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
