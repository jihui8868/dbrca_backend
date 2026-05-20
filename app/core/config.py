"""Configuration management for multi-database RCA application"""
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class DatabaseConfig:
    """Universal database configuration supporting multiple database types"""

    # Database type detection
    database_type: str = os.getenv("DATABASE_TYPE", "mysql")  # mysql, postgresql, informix

    # Connection parameters
    host: str = os.getenv("DB_HOST", "localhost")
    port: int = int(os.getenv("DB_PORT", "3306"))
    user: str = os.getenv("DB_USER", "root")
    password: str = os.getenv("DB_PASSWORD", "")
    database: str = os.getenv("DB_NAME", "mysql")

    # Connection pool
    pool_size: int = int(os.getenv("DB_POOL_SIZE", "5"))
    max_overflow: int = int(os.getenv("DB_MAX_OVERFLOW", "10"))

    # Custom DSN (overrides other parameters if provided)
    custom_dsn: Optional[str] = os.getenv("DATABASE_URL")

    @property
    def dsn(self) -> str:
        """Generate database connection string based on database type"""
        # If custom DSN is provided, use it
        if self.custom_dsn:
            return self.custom_dsn

        db_type = self.database_type.lower()

        # MySQL/MariaDB
        if db_type in ("mysql", "mariadb"):
            driver = "pymysql"
            return (
                f"{db_type}+{driver}://{self.user}:{self.password}@"
                f"{self.host}:{self.port}/{self.database}"
            )

        # PostgreSQL
        elif db_type == "postgresql":
            driver = "psycopg2"  # or psycopg2-binary
            return (
                f"postgresql+{driver}://{self.user}:{self.password}@"
                f"{self.host}:{self.port}/{self.database}"
            )

        # Informix
        elif db_type == "informix":
            # Informix requires special handling
            return (
                f"informix+pyodbc://{self.user}:{self.password}@"
                f"{self.host}:{self.port}/{self.database}"
            )

        # Oracle
        elif db_type == "oracle":
            return (
                f"oracle+cx_oracle://{self.user}:{self.password}@"
                f"{self.host}:{self.port}/{self.database}"
            )

        # SQL Server
        elif db_type == "sqlserver":
            driver = "pymssql"
            return (
                f"mssql+{driver}://{self.user}:{self.password}@"
                f"{self.host}:{self.port}/{self.database}"
            )

        else:
            raise ValueError(f"Unsupported database type: {db_type}")


@dataclass
class LLMConfig:
    """Universal LLM configuration supporting OpenAI, Deepseek, and others"""

    # Provider options: openai, deepseek, anthropic, ollama, etc.
    provider: str = os.getenv("LLM_PROVIDER", "deepseek")

    # Model selection (format: "provider:model-name")
    # Examples:
    #   openai:gpt-4
    #   openai:gpt-4-turbo
    #   deepseek:deepseek-chat
    #   deepseek:deepseek-coder
    #   anthropic:claude-opus-4
    model: str = os.getenv("LLM_MODEL", "deepseek:deepseek-chat")

    # API Keys (different providers use different env vars)
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    deepseek_api_key: str = os.getenv("DEEPSEEK_API_KEY", "")
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")

    # Deepseek specific
    deepseek_base_url: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

    # Model parameters
    temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    max_tokens: int = int(os.getenv("LLM_MAX_TOKENS", "2048"))
    top_p: float = float(os.getenv("LLM_TOP_P", "1.0"))
    timeout: int = int(os.getenv("LLM_TIMEOUT", "30"))

    # Retry configuration
    max_retries: int = int(os.getenv("LLM_MAX_RETRIES", "3"))

    @property
    def api_key(self) -> str:
        """Get API key for the configured provider"""
        provider = self.provider.lower()

        if provider == "openai":
            return self.openai_api_key
        elif provider == "deepseek":
            return self.deepseek_api_key
        elif provider == "anthropic":
            return self.anthropic_api_key
        else:
            return self.openai_api_key  # Default fallback


@dataclass
class AgentConfig:
    """Multi-agent configuration"""
    max_iterations: int = int(os.getenv("AGENT_MAX_ITERATIONS", "10"))
    timeout: int = int(os.getenv("AGENT_TIMEOUT", "300"))
    verbose: bool = os.getenv("AGENT_VERBOSE", "false").lower() == "true"
    debug: bool = os.getenv("AGENT_DEBUG", "false").lower() == "true"


class Settings:
    """Global settings"""
    database: DatabaseConfig = DatabaseConfig()
    llm: LLMConfig = LLMConfig()
    agent: AgentConfig = AgentConfig()


settings = Settings()
