# Quick Start: Switching LLM Providers

This guide shows how to quickly switch between different LLM providers without modifying code.

## Prerequisites

Install the backend with all optional dependencies:

```bash
pip install -e .[all]
```

Or install specific provider support:

```bash
pip install -e .[anthropic]      # For Anthropic Claude
pip install -e .[ollama]          # For Ollama local LLMs
pip install -e .[all-llms]        # For all LLM providers
```

## 1. OpenAI (Default)

The system comes configured for OpenAI by default.

### Setup

1. Get your API key from [OpenAI](https://platform.openai.com/api-keys)
2. Set environment variables:

```bash
export LLM_PROVIDER=openai
export LLM_MODEL=openai:gpt-4
export OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxx
```

3. Run the diagnostic:

```bash
python main.py
```

### Model Options

```bash
# Most capable (recommended for production)
export LLM_MODEL=openai:gpt-4

# Faster and cheaper
export LLM_MODEL=openai:gpt-4-turbo

# Budget option
export LLM_MODEL=openai:gpt-3.5-turbo
```

## 2. Deepseek (Cost-Efficient)

Deepseek offers excellent value with competitive performance.

### Setup

1. Get your API key from [Deepseek](https://platform.deepseek.com/api-keys)
2. Set environment variables:

```bash
export LLM_PROVIDER=deepseek
export LLM_MODEL=deepseek:deepseek-chat
export DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxx
```

3. Run the diagnostic:

```bash
python main.py
```

### Model Options

```bash
# General purpose (recommended)
export LLM_MODEL=deepseek:deepseek-chat

# Code-focused
export LLM_MODEL=deepseek:deepseek-coder
```

## 3. Anthropic Claude (Advanced Reasoning)

Anthropic Claude excels at complex reasoning tasks.

### Setup

1. Get your API key from [Anthropic](https://console.anthropic.com/)
2. Install provider support:

```bash
pip install -e .[anthropic]
```

3. Set environment variables:

```bash
export LLM_PROVIDER=anthropic
export LLM_MODEL=anthropic:claude-opus-4
export ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxx
```

4. Run the diagnostic:

```bash
python main.py
```

### Model Options

```bash
# Most capable (recommended)
export LLM_MODEL=anthropic:claude-opus-4

# Faster
export LLM_MODEL=anthropic:claude-sonnet

# Budget option
export LLM_MODEL=anthropic:claude-haiku
```

## 4. Ollama (Local, No API Key)

Run local LLMs on your machine - perfect for development.

### Setup

1. Install and start Ollama:

```bash
# Download from https://ollama.ai
ollama serve
```

This starts Ollama on http://localhost:11434

2. In another terminal, set environment variables:

```bash
export LLM_PROVIDER=ollama
export LLM_MODEL=ollama:llama2
```

3. Run the diagnostic:

```bash
python main.py
```

### Available Models

```bash
# Pull a model
ollama pull llama2
ollama pull mistral
ollama pull neural-chat

# Use it
export LLM_MODEL=ollama:llama2
python main.py
```

## Switching Providers

### Method 1: Environment Variables (Recommended)

```bash
# Switch to Deepseek
export LLM_PROVIDER=deepseek
export LLM_MODEL=deepseek:deepseek-chat
export DEEPSEEK_API_KEY=sk-xxx...
python main.py

# Switch back to OpenAI
export LLM_PROVIDER=openai
export LLM_MODEL=openai:gpt-4
export OPENAI_API_KEY=sk-xxx...
python main.py
```

### Method 2: Using .env File

Create a `.env` file (do not commit this to Git):

```bash
# .env
LLM_PROVIDER=deepseek
LLM_MODEL=deepseek:deepseek-chat
DEEPSEEK_API_KEY=sk-xxx...

DATABASE_TYPE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=testdb
```

Then run:

```bash
python main.py  # Automatically loads from .env
```

## Troubleshooting

### "API_KEY environment variable not set"

```bash
# Check if the environment variable is set
echo $OPENAI_API_KEY    # for OpenAI
echo $DEEPSEEK_API_KEY  # for Deepseek
echo $ANTHROPIC_API_KEY # for Anthropic

# Set it if missing
export OPENAI_API_KEY=sk-xxx...
```

### "No module named 'langchain_anthropic'"

Install the provider:

```bash
pip install -e .[anthropic]
```

### "Connection refused" (for Ollama)

Make sure Ollama is running:

```bash
# In another terminal
ollama serve
```

### "Unsupported LLM provider"

Check your `LLM_PROVIDER` setting:

```bash
# Valid options: openai, deepseek, anthropic, ollama
export LLM_PROVIDER=openai
```

## Performance Comparison

| Provider | Speed | Cost | Best For |
|----------|-------|------|----------|
| OpenAI (GPT-4) | Medium | High | Production |
| Deepseek | Fast | Low | Development |
| Anthropic | Medium | Medium | Complex reasoning |
| Ollama | Varies | Free | Local development |

## Cost Estimation

For a typical database diagnostic (2000 tokens input, 1000 tokens output):

- **OpenAI (gpt-4):** ~$0.12
- **Deepseek:** ~$0.001
- **Anthropic (claude-opus-4):** ~$0.09
- **Ollama:** Free (local)

## Production Recommendations

1. **Use OpenAI GPT-4** for reliability in production
2. **Use Deepseek** for cost-sensitive environments
3. **Use Anthropic Claude** for complex analysis tasks
4. **Use Ollama** for development and testing

## Complete Example: Switching from OpenAI to Deepseek

```bash
# Currently using OpenAI
echo $LLM_PROVIDER  # openai
python main.py      # Works with OpenAI

# Switch to Deepseek
export LLM_PROVIDER=deepseek
export LLM_MODEL=deepseek:deepseek-chat
export DEEPSEEK_API_KEY=sk-xxx...

# No code changes needed!
python main.py  # Now uses Deepseek

# Switch back
export LLM_PROVIDER=openai
export LLM_MODEL=openai:gpt-4
export OPENAI_API_KEY=sk-xxx...

python main.py  # Back to OpenAI
```

## Next Steps

- Read [LLM_INTEGRATION_SUMMARY.md](./LLM_INTEGRATION_SUMMARY.md) for detailed information
- Check [README.md](./README.md) for project overview
- See [MULTI_DATABASE_SUPPORT.md](./MULTI_DATABASE_SUPPORT.md) for database switching
