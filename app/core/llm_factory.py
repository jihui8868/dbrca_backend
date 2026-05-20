"""LLM Factory for creating different LLM providers"""
from typing import Union
from langchain.chat_models import BaseChatModel
from .config import settings


def create_llm(
    provider: str = None,
    model: str = None,
    api_key: str = None,
    **kwargs
) -> BaseChatModel:
    """
    Create an LLM instance based on provider and model.

    Args:
        provider: LLM provider (openai, deepseek, anthropic, etc.)
        model: Model name (e.g., gpt-4, deepseek-chat, claude-opus-4)
        api_key: API key for authentication
        **kwargs: Additional parameters to pass to the LLM

    Returns:
        Initialized BaseChatModel instance
    """
    provider = provider or settings.llm.provider
    model = model or settings.llm.model
    api_key = api_key or settings.llm.api_key

    # Parse model string if it contains provider prefix (e.g., "openai:gpt-4")
    if ":" in model:
        model_provider, model_name = model.split(":", 1)
        if not provider or provider == "auto":
            provider = model_provider
        model = model_name

    provider = provider.lower()

    print(f"🤖 Initializing {provider.upper()} LLM: {model}")

    if provider == "openai":
        return _create_openai_llm(model, api_key, **kwargs)

    elif provider == "deepseek":
        return _create_deepseek_llm(model, api_key, **kwargs)

    elif provider == "anthropic":
        return _create_anthropic_llm(model, api_key, **kwargs)

    elif provider == "ollama":
        return _create_ollama_llm(model, **kwargs)

    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")


def _create_openai_llm(model: str, api_key: str, **kwargs) -> BaseChatModel:
    """Create OpenAI ChatGPT LLM"""
    from langchain_openai import ChatOpenAI

    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    return ChatOpenAI(
        model=model,
        api_key=api_key,
        temperature=kwargs.get("temperature", settings.llm.temperature),
        max_tokens=kwargs.get("max_tokens", settings.llm.max_tokens),
        timeout=kwargs.get("timeout", settings.llm.timeout),
        max_retries=kwargs.get("max_retries", settings.llm.max_retries),
    )


def _create_deepseek_llm(model: str, api_key: str, **kwargs) -> BaseChatModel:
    """Create Deepseek LLM"""
    from langchain_openai import ChatOpenAI

    if not api_key:
        raise ValueError("DEEPSEEK_API_KEY environment variable not set")

    # Deepseek uses OpenAI-compatible API
    return ChatOpenAI(
        model=model,
        api_key=api_key,
        base_url=kwargs.get("base_url", settings.llm.deepseek_base_url),
        temperature=kwargs.get("temperature", settings.llm.temperature),
        max_tokens=kwargs.get("max_tokens", settings.llm.max_tokens),
        timeout=kwargs.get("timeout", settings.llm.timeout),
        max_retries=kwargs.get("max_retries", settings.llm.max_retries),
    )


def _create_anthropic_llm(model: str, api_key: str, **kwargs) -> BaseChatModel:
    """Create Anthropic Claude LLM"""
    try:
        from langchain_anthropic import ChatAnthropic

        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        return ChatAnthropic(
            model=model,
            api_key=api_key,
            temperature=kwargs.get("temperature", settings.llm.temperature),
            max_tokens=kwargs.get("max_tokens", settings.llm.max_tokens),
            timeout=kwargs.get("timeout", settings.llm.timeout),
        )
    except ImportError:
        raise ImportError(
            "langchain-anthropic not installed. "
            "Install it with: pip install langchain-anthropic"
        )


def _create_ollama_llm(model: str, **kwargs) -> BaseChatModel:
    """Create Ollama local LLM"""
    try:
        from langchain_ollama import ChatOllama

        return ChatOllama(
            model=model,
            base_url=kwargs.get("base_url", "http://localhost:11434"),
            temperature=kwargs.get("temperature", settings.llm.temperature),
            num_ctx=kwargs.get("num_ctx", 2048),
        )
    except ImportError:
        raise ImportError(
            "langchain-ollama not installed. "
            "Install it with: pip install langchain-ollama"
        )


def get_default_llm() -> BaseChatModel:
    """Get the default LLM configured in settings"""
    return create_llm(
        provider=settings.llm.provider,
        model=settings.llm.model,
        api_key=settings.llm.api_key,
    )


# Convenience functions for common providers

def get_openai(model: str = "gpt-4", api_key: str = None) -> BaseChatModel:
    """Quickly create an OpenAI ChatGPT LLM"""
    return create_llm(provider="openai", model=model, api_key=api_key)


def get_deepseek(model: str = "deepseek-chat", api_key: str = None) -> BaseChatModel:
    """Quickly create a Deepseek LLM"""
    return create_llm(provider="deepseek", model=model, api_key=api_key)


def get_anthropic(model: str = "claude-opus-4", api_key: str = None) -> BaseChatModel:
    """Quickly create an Anthropic Claude LLM"""
    return create_llm(provider="anthropic", model=model, api_key=api_key)


def get_ollama(model: str = "llama2") -> BaseChatModel:
    """Quickly create an Ollama local LLM"""
    return create_llm(provider="ollama", model=model)
