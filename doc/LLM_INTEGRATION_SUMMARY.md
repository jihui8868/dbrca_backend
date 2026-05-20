# Multi-LLM Integration Summary

## Overview

The RCA system has been successfully enhanced to support **multiple LLM providers** alongside the existing **multi-database architecture**. The system now provides a flexible, extensible platform for AI-driven database diagnostics.

## Completed Features

### 1. LLM Factory Pattern Implementation

**File:** `app/core/llm_factory.py`

The factory pattern provides a unified interface for creating LLM instances across multiple providers:

```python
# Automatic provider detection
llm = create_llm(provider="deepseek", model="deepseek-chat", api_key="sk-xxx...")

# Convenience functions for common providers
openai_llm = get_openai(model="gpt-4", api_key="sk-xxx...")
deepseek_llm = get_deepseek(model="deepseek-chat", api_key="sk-xxx...")
anthropic_llm = get_anthropic(model="claude-opus-4", api_key="sk-ant-xxx...")
ollama_llm = get_ollama(model="llama2")
```

**Supported Providers:**
- ✅ OpenAI (gpt-4, gpt-4-turbo, gpt-3.5-turbo, etc.)
- ✅ Deepseek (deepseek-chat, deepseek-coder, etc.)
- ✅ Anthropic Claude (claude-opus-4, claude-sonnet, etc.)
- ✅ Ollama (local LLMs like llama2, mistral, etc.)

### 2. Configuration System (`app/core/config.py`)

The LLMConfig class supports flexible configuration:

```python
# Provider-specific settings
LLM_PROVIDER=openai                    # or deepseek, anthropic, ollama
LLM_MODEL=openai:gpt-4                 # format: "provider:model-name"
OPENAI_API_KEY=sk-xxx...               # OpenAI API key
DEEPSEEK_API_KEY=sk-xxx...             # Deepseek API key
ANTHROPIC_API_KEY=sk-ant-xxx...        # Anthropic API key
DEEPSEEK_BASE_URL=https://api.deepseek.com  # Custom base URL (optional)

# Model parameters (universal across all providers)
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2048
LLM_TOP_P=1.0
LLM_TIMEOUT=30
LLM_MAX_RETRIES=3
```

### 3. Main Agent Integration (`app/agents/main_agent.py`)

The main RCA agent now uses the LLM factory:

```python
def create_rca_agent():
    """Create the main RCA agent with all sub-agents"""
    
    # Use factory to create LLM based on configuration
    llm = create_llm(
        provider=settings.llm.provider,
        model=settings.llm.model,
        api_key=settings.llm.api_key,
    )
    
    # Pass LLM instance to deepagents
    agent = create_deep_agent(
        model=llm,  # Now accepts LLM instance, not model string
        system_prompt=system_prompt,
        subagents=[
            performance_analyzer,
            log_analyzer,
            query_analyzer,
            config_inspector,
        ],
    )
    
    return agent
```

### 4. Updated Configuration Files

#### `.env.example` - Environment Configuration

Now includes complete LLM provider examples:

```bash
# Provider selection
LLM_PROVIDER=openai  # or deepseek, anthropic, ollama

# Provider-specific API keys
OPENAI_API_KEY=your_openai_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Model parameters
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2048
```

#### `pyproject.toml` - Package Dependencies

Added optional dependencies for each LLM provider:

```toml
[project.optional-dependencies]
# LLM Providers
anthropic = ["langchain-anthropic>=0.2.0"]
ollama = ["langchain-ollama>=0.1.0"]
all-llms = [
    "langchain-anthropic>=0.2.0",
    "langchain-ollama>=0.1.0",
]

# Complete setup with all providers and drivers
all = [
    "langchain-anthropic>=0.2.0",
    "langchain-ollama>=0.1.0",
    "psycopg2-binary>=2.9.0",
    "pyodbc>=4.1.0",
    "cx_oracle>=8.3.0",
    "pymssql>=2.2.0",
]
```

**Installation Options:**
```bash
# Install with specific LLM provider
pip install -e .[anthropic]          # For Anthropic support
pip install -e .[ollama]              # For Ollama support
pip install -e .[all-llms]            # For all LLM providers
pip install -e .[all]                 # Everything (all providers + databases)
```

### 5. Testing and Validation

**File:** `test_integration.py`

Comprehensive integration tests verify:

✅ Configuration loading and provider selection
✅ LLM factory provider parsing (e.g., "deepseek:deepseek-chat")
✅ API key resolution for each provider
✅ Agent creation with LLM factory integration
✅ Database connection and dialect selection

**Run tests:**
```bash
./.venv/bin/python test_integration.py
```

## Architecture: Multi-Provider + Multi-Database

```
┌─────────────────────────────────────────────────────────┐
│           Main RCA Agent (create_rca_agent)             │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
    LLM Factory          Sub-Agents (4)
    ├─ OpenAI           ├─ performance-analyzer
    ├─ Deepseek         ├─ log-analyzer
    ├─ Anthropic        ├─ query-analyzer
    └─ Ollama           └─ config-inspector
        │                         │
        └────────────┬────────────┘
                     │
            ┌────────┴────────┐
            │                 │
            ▼                 ▼
        LLM Model      Database Manager
                       ├─ MySQL Dialect
                       ├─ PostgreSQL Dialect
                       ├─ Informix Dialect
                       └─ Oracle Dialect
```

## Provider Comparison

| Feature | OpenAI | Deepseek | Anthropic | Ollama |
|---------|--------|----------|-----------|--------|
| Cloud/Local | Cloud | Cloud | Cloud | Local |
| API Type | Native | OpenAI-compatible | Langchain | Langchain |
| Cost | Higher | Lower | Higher | Free |
| Models | GPT-4, GPT-3.5 | deepseek-chat, coder | Claude series | llama2, mistral |
| Latency | Medium | Low | Medium | Varies |
| Best For | Production | Cost-efficient | Advanced | Development |

## Configuration Examples

### Example 1: Using OpenAI (Default)

```bash
export LLM_PROVIDER=openai
export LLM_MODEL=openai:gpt-4
export OPENAI_API_KEY=sk-xxx...

python main.py
```

### Example 2: Using Deepseek

```bash
export LLM_PROVIDER=deepseek
export LLM_MODEL=deepseek:deepseek-chat
export DEEPSEEK_API_KEY=sk-xxx...

python main.py
```

### Example 3: Using Anthropic Claude

```bash
export LLM_PROVIDER=anthropic
export LLM_MODEL=anthropic:claude-opus-4
export ANTHROPIC_API_KEY=sk-ant-xxx...
pip install -e .[anthropic]

python main.py
```

### Example 4: Using Local Ollama

```bash
# Start Ollama (in another terminal)
ollama serve

# Configure and run
export LLM_PROVIDER=ollama
export LLM_MODEL=ollama:llama2

python main.py
```

## Switching Providers at Runtime

```python
# Without code changes - just environment variables
export LLM_PROVIDER=deepseek
export DEEPSEEK_API_KEY=sk-xxx...

# The system automatically loads the correct provider:
from app.core.llm_factory import create_llm
from app.core.config import settings

llm = create_llm(
    provider=settings.llm.provider,      # deepseek
    model=settings.llm.model,            # deepseek-chat
    api_key=settings.llm.api_key,        # uses DEEPSEEK_API_KEY
)
```

## Error Handling

The factory pattern includes proper validation:

```python
# Missing API key
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set")

# Unsupported provider
raise ValueError(f"Unsupported LLM provider: {provider}")

# Import errors (for optional dependencies)
try:
    from langchain_anthropic import ChatAnthropic
except ImportError:
    raise ImportError(
        "langchain-anthropic not installed. "
        "Install it with: pip install langchain-anthropic"
    )
```

## Deployment Recommendations

### Development
- Use Ollama locally for fast iteration
- No API keys required
- Suitable for testing and debugging

### Staging
- Use Deepseek for cost-efficient testing
- Good balance of cost and performance
- Validate with production-like models

### Production
- Use OpenAI (gpt-4) for reliability
- Or Anthropic Claude for advanced reasoning
- Set up proper rate limiting and retry policies

## Monitoring and Logging

The system logs LLM initialization:

```
🤖 Initializing OPENAI LLM: gpt-4
🤖 Initializing DEEPSEEK LLM: deepseek-chat
🤖 Initializing ANTHROPIC LLM: claude-opus-4
🤖 Initializing OLLAMA LLM: llama2
```

## Future Enhancements

1. **LLM Caching:** Add response caching to reduce API calls
2. **Load Balancing:** Round-robin between multiple LLM instances
3. **Cost Tracking:** Monitor and report API usage costs
4. **Fallback Chain:** Automatic fallback to another provider on failure
5. **Model Versioning:** Track and manage different model versions

## Testing Verification

Run the integration tests to verify everything is working:

```bash
./.venv/bin/python test_integration.py
```

Expected output:
```
✓ Configuration loaded
✓ LLM factory working
✓ Agent creation validated
✓ Database dialect detected
```

## Summary

The RCA system now provides:

✅ **Flexible LLM Provider Support** - Choose from OpenAI, Deepseek, Anthropic, or Ollama
✅ **Easy Configuration** - Environment variables for quick switching
✅ **Factory Pattern** - Clean, extensible architecture for adding new providers
✅ **Multi-Database Support** - MySQL, PostgreSQL, Informix, Oracle, SQL Server
✅ **deepagents Integration** - Multi-agent orchestration for comprehensive diagnostics
✅ **Production Ready** - Error handling, validation, and comprehensive testing

The system can be deployed in any configuration:
- Different databases with different LLM providers
- Multiple instances for high availability
- Easy switching between providers based on requirements
