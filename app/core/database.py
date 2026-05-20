"""Universal database connection management supporting multiple database types"""
from typing import Optional, Dict, List, Any
from sqlalchemy import create_engine, text, MetaData
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool, NullPool

from .config import settings
from .database_types import (
    DatabaseType,
    get_dialect,
    detect_database_type,
    DatabaseDialect,
)


class UniversalDatabaseManager:
    """
    Universal database manager supporting MySQL, PostgreSQL, Informix, and others.
    Uses strategy pattern to handle different database dialects.
    """

    def __init__(self, dsn: Optional[str] = None):
        """
        Initialize database manager

        Args:
            dsn: Database connection string. If not provided, uses settings.database.dsn
        """
        self.dsn = dsn or settings.database.dsn
        self.db_type = detect_database_type(self.dsn)
        self.dialect = get_dialect(self.db_type)

        self.engine = None
        self.SessionLocal = None
        self.metadata = MetaData()

        self._initialize_engine()

    def _initialize_engine(self):
        """Initialize SQLAlchemy engine with database-specific settings"""
        # Get database-specific connection arguments
        connect_args = self.dialect.get_connection_args()

        # Additional standard arguments
        connect_args.update({
            "connect_timeout": 10,
        })

        # Select appropriate connection pool
        pool_class = QueuePool
        pool_kwargs = {
            "pool_size": settings.database.pool_size,
            "max_overflow": settings.database.max_overflow,
        }

        # PostgreSQL often works better with NullPool in certain scenarios
        if self.db_type == DatabaseType.POSTGRESQL:
            pool_class = QueuePool

        self.engine = create_engine(
            self.dsn,
            poolclass=pool_class,
            echo=settings.agent.debug,
            connect_args=connect_args,
            **pool_kwargs
        )

        self.SessionLocal = sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
        )

    def get_session(self) -> Session:
        """Get a new database session"""
        return self.SessionLocal()

    def test_connection(self) -> bool:
        """Test database connectivity"""
        try:
            with self.get_session() as session:
                session.execute(text("SELECT 1"))
            print(f"✓ Connected to {self.db_type.value} database")
            return True
        except Exception as e:
            print(f"✗ Database connection failed: {e}")
            return False

    def execute_query(self, query: str, session: Optional[Session] = None) -> List[Dict[str, Any]]:
        """
        Execute a read query

        Args:
            query: SQL query to execute
            session: Optional existing session

        Returns:
            List of dictionaries with query results
        """
        should_close = False
        if session is None:
            session = self.get_session()
            should_close = True

        try:
            result = session.execute(text(query))
            rows = result.fetchall()
            columns = result.keys()
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            print(f"Query execution error: {e}")
            return []
        finally:
            if should_close:
                session.close()

    def execute_command(self, command: str, session: Optional[Session] = None) -> bool:
        """
        Execute a write command (INSERT, UPDATE, DELETE)

        Args:
            command: SQL command to execute
            session: Optional existing session

        Returns:
            True if successful, False otherwise
        """
        should_close = False
        if session is None:
            session = self.get_session()
            should_close = True

        try:
            session.execute(text(command))
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Command execution failed: {e}")
            return False
        finally:
            if should_close:
                session.close()

    def get_database_size(self) -> List[Dict[str, Any]]:
        """Get database size information using dialect-specific query"""
        query = self.dialect.get_database_size_query()
        return self.execute_query(query)

    def get_slow_queries(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get slow queries using dialect-specific query"""
        try:
            query = self.dialect.get_slow_queries_query(limit)
            return self.execute_query(query)
        except Exception as e:
            print(f"Failed to fetch slow queries: {e}")
            return []

    def get_table_statistics(self) -> List[Dict[str, Any]]:
        """Get table statistics using dialect-specific query"""
        try:
            query = self.dialect.get_table_statistics_query()
            return self.execute_query(query)
        except Exception as e:
            print(f"Failed to fetch table statistics: {e}")
            return []

    def get_process_list(self) -> List[Dict[str, Any]]:
        """Get current process list using dialect-specific query"""
        try:
            query = self.dialect.get_process_list_query()
            return self.execute_query(query)
        except Exception as e:
            print(f"Failed to fetch process list: {e}")
            return []

    def get_lock_info(self) -> List[Dict[str, Any]]:
        """Get lock information using dialect-specific query"""
        try:
            query = self.dialect.get_lock_info_query()
            return self.execute_query(query)
        except Exception as e:
            print(f"Failed to fetch lock info: {e}")
            return []

    def get_error_log(self) -> List[Dict[str, Any]]:
        """Get error log information using dialect-specific query"""
        try:
            query = self.dialect.get_error_log_query()
            return self.execute_query(query)
        except Exception as e:
            print(f"Failed to fetch error log: {e}")
            return []

    def get_cache_efficiency(self) -> List[Dict[str, Any]]:
        """Get cache efficiency metrics using dialect-specific query"""
        try:
            query = self.dialect.get_cache_efficiency_query()
            return self.execute_query(query)
        except Exception as e:
            print(f"Failed to fetch cache efficiency: {e}")
            return []

    def get_index_usage(self) -> List[Dict[str, Any]]:
        """Get index usage statistics using dialect-specific query"""
        try:
            query = self.dialect.get_index_usage_query()
            return self.execute_query(query)
        except Exception as e:
            print(f"Failed to fetch index usage: {e}")
            return []

    def get_variable(self, var_name: str) -> Optional[str]:
        """Get configuration variable value"""
        try:
            query = self.dialect.get_configuration_query(var_name)
            results = self.execute_query(query)
            if results:
                # Database-specific result parsing
                if self.db_type == DatabaseType.MYSQL:
                    return results[0].get('Value')
                elif self.db_type == DatabaseType.POSTGRESQL:
                    return results[0].get('setting')
                else:
                    return results[0].get('value')
            return None
        except Exception as e:
            print(f"Failed to fetch variable {var_name}: {e}")
            return None

    def get_database_info(self) -> Dict[str, Any]:
        """Get database information"""
        return {
            "type": self.db_type.value,
            "host": self.engine.url.host,
            "port": self.engine.url.port,
            "database": self.engine.url.database,
            "user": self.engine.url.username,
        }

    def close(self):
        """Close database connections"""
        if self.engine:
            self.engine.dispose()


# Global database manager instance
db_manager = UniversalDatabaseManager()
