"""Database connection management"""
import pymysql
from typing import Optional, Dict, List, Any
from sqlalchemy import create_engine, text, MetaData
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool

from .config import settings


class DatabaseManager:
    """Manages MySQL database connections and operations"""

    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self.metadata = MetaData()
        self._initialize_engine()

    def _initialize_engine(self):
        """Initialize SQLAlchemy engine"""
        self.engine = create_engine(
            settings.database.dsn,
            poolclass=QueuePool,
            pool_size=settings.database.pool_size,
            max_overflow=settings.database.max_overflow,
            echo=settings.agent.debug,
            connect_args={
                "charset": "utf8mb4",
                "connect_timeout": 10,
            }
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
            return True
        except Exception as e:
            print(f"Database connection failed: {e}")
            return False

    def execute_query(self, query: str, session: Optional[Session] = None) -> List[Dict[str, Any]]:
        """Execute a read query"""
        should_close = False
        if session is None:
            session = self.get_session()
            should_close = True

        try:
            result = session.execute(text(query))
            rows = result.fetchall()
            columns = result.keys()
            return [dict(zip(columns, row)) for row in rows]
        finally:
            if should_close:
                session.close()

    def execute_command(self, command: str, session: Optional[Session] = None) -> bool:
        """Execute a write command"""
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

    def get_database_size(self) -> Dict[str, Any]:
        """Get database size information"""
        query = """
        SELECT
            table_schema,
            ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) as size_mb
        FROM information_schema.tables
        GROUP BY table_schema
        """
        return self.execute_query(query)

    def get_slow_queries(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get slow queries from performance schema"""
        query = f"""
        SELECT
            digest_text,
            count_star,
            avg_timer_wait / 1000000000000 as avg_time_sec,
            max_timer_wait / 1000000000000 as max_time_sec
        FROM performance_schema.events_statements_summary_by_digest
        ORDER BY sum_timer_wait DESC
        LIMIT {limit}
        """
        try:
            return self.execute_query(query)
        except Exception as e:
            print(f"Failed to fetch slow queries: {e}")
            return []

    def get_table_statistics(self) -> List[Dict[str, Any]]:
        """Get table statistics"""
        query = """
        SELECT
            table_schema,
            table_name,
            table_rows,
            ROUND(((data_length + index_length) / 1024 / 1024), 2) as size_mb,
            ROUND((data_free / 1024 / 1024), 2) as free_mb
        FROM information_schema.tables
        WHERE table_schema NOT IN ('mysql', 'information_schema', 'performance_schema', 'sys')
        """
        return self.execute_query(query)

    def get_process_list(self) -> List[Dict[str, Any]]:
        """Get current MySQL process list"""
        query = """
        SELECT
            id,
            user,
            host,
            db,
            command,
            time,
            state,
            left(info, 100) as info
        FROM information_schema.processlist
        ORDER BY time DESC
        """
        return self.execute_query(query)

    def get_lock_info(self) -> List[Dict[str, Any]]:
        """Get lock information"""
        query = """
        SELECT
            waiting_trx_id,
            waiting_pid,
            waiting_query,
            blocking_trx_id,
            blocking_pid,
            blocking_query
        FROM sys.innodb_lock_waits
        """
        try:
            return self.execute_query(query)
        except Exception as e:
            print(f"Failed to fetch lock info: {e}")
            return []

    def get_variable(self, var_name: str) -> Optional[str]:
        """Get MySQL variable value"""
        query = f"SHOW VARIABLES LIKE '{var_name}'"
        result = self.execute_query(query)
        return result[0]['Value'] if result else None

    def close(self):
        """Close database connections"""
        if self.engine:
            self.engine.dispose()


db_manager = DatabaseManager()
