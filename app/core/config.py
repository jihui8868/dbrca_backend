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
