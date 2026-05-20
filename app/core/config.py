"""Configuration management for MySQL RCA application"""
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class DatabaseConfig:
    """MySQL database configuration"""
    host: str = os.getenv("MYSQL_HOST", "localhost")
    port: int = int(os.getenv("MYSQL_PORT", "3306"))
    user: str = os.getenv("MYSQL_USER", "root")
    password: str = os.getenv("MYSQL_PASSWORD", "")
    database: str = os.getenv("MYSQL_DATABASE", "mysql")
    pool_size: int = int(os.getenv("MYSQL_POOL_SIZE", "5"))
    max_overflow: int = int(os.getenv("MYSQL_MAX_OVERFLOW", "10"))

    @property
    def dsn(self) -> str:
        """Database connection string"""
        return (
            f"mysql+pymysql://{self.user}:{self.password}@"
            f"{self.host}:{self.port}/{self.database}"
        )


@dataclass
class LLMConfig:
    """LLM configuration"""
    model: str = os.getenv("LLM_MODEL", "gpt-4")
    api_key: str = os.getenv("OPENAI_API_KEY", "")
    temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    max_tokens: int = int(os.getenv("LLM_MAX_TOKENS", "2048"))


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
