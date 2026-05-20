"""Database type definitions and support"""
from enum import Enum
from typing import Dict, List, Tuple


class DatabaseType(Enum):
    """Supported database types"""
    MYSQL = "mysql"
    POSTGRESQL = "postgresql"
    INFORMIX = "informix"
    MARIADB = "mariadb"
    ORACLE = "oracle"
    SQLSERVER = "sqlserver"


class DatabaseDialect:
    """Base class for database-specific SQL dialects and metadata queries"""

    def __init__(self):
        self.db_type: DatabaseType = None

    def get_database_size_query(self) -> str:
        """Get database size query for this database type"""
        raise NotImplementedError

    def get_slow_queries_query(self, limit: int = 10) -> str:
        """Get slow queries for this database type"""
        raise NotImplementedError

    def get_table_statistics_query(self) -> str:
        """Get table statistics for this database type"""
        raise NotImplementedError

    def get_process_list_query(self) -> str:
        """Get current process list for this database type"""
        raise NotImplementedError

    def get_lock_info_query(self) -> str:
        """Get lock information for this database type"""
        raise NotImplementedError

    def get_error_log_query(self) -> str:
        """Get error log information for this database type"""
        raise NotImplementedError

    def get_cache_efficiency_query(self) -> str:
        """Get cache efficiency metrics for this database type"""
        raise NotImplementedError

    def get_index_usage_query(self) -> str:
        """Get index usage statistics for this database type"""
        raise NotImplementedError

    def get_configuration_query(self, param_name: str = None) -> str:
        """Get configuration parameters for this database type"""
        raise NotImplementedError

    def get_connection_args(self) -> Dict:
        """Get database-specific connection arguments"""
        return {}


class MySQLDialect(DatabaseDialect):
    """MySQL-specific SQL dialect"""

    def __init__(self):
        super().__init__()
        self.db_type = DatabaseType.MYSQL

    def get_database_size_query(self) -> str:
        return """
        SELECT
            table_schema as schema_name,
            ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) as size_mb
        FROM information_schema.tables
        WHERE table_type = 'BASE TABLE'
        GROUP BY table_schema
        ORDER BY size_mb DESC
        """

    def get_slow_queries_query(self, limit: int = 10) -> str:
        return f"""
        SELECT
            digest_text as query,
            count_star as execution_count,
            avg_timer_wait / 1000000000000 as avg_time_sec,
            max_timer_wait / 1000000000000 as max_time_sec
        FROM performance_schema.events_statements_summary_by_digest
        WHERE digest_text IS NOT NULL
        ORDER BY sum_timer_wait DESC
        LIMIT {limit}
        """

    def get_table_statistics_query(self) -> str:
        return """
        SELECT
            table_schema as schema_name,
            table_name,
            table_rows as row_count,
            ROUND(((data_length + index_length) / 1024 / 1024), 2) as size_mb,
            ROUND((data_free / 1024 / 1024), 2) as free_mb
        FROM information_schema.tables
        WHERE table_schema NOT IN ('mysql', 'information_schema', 'performance_schema', 'sys')
        AND table_type = 'BASE TABLE'
        ORDER BY size_mb DESC
        """

    def get_process_list_query(self) -> str:
        return """
        SELECT
            id,
            user,
            host,
            db as database_name,
            command,
            time as duration_sec,
            state,
            LEFT(info, 100) as query
        FROM information_schema.processlist
        WHERE command != 'Sleep'
        ORDER BY time DESC
        """

    def get_lock_info_query(self) -> str:
        return """
        SELECT
            waiting_trx_id,
            waiting_pid,
            waiting_query,
            blocking_trx_id,
            blocking_pid,
            blocking_query
        FROM sys.innodb_lock_waits
        """

    def get_error_log_query(self) -> str:
        return """
        SELECT
            variable_name,
            variable_value
        FROM performance_schema.global_status
        WHERE variable_name IN (
            'Aborted_clients',
            'Aborted_connects',
            'Errors',
            'Warnings'
        )
        """

    def get_cache_efficiency_query(self) -> str:
        return """
        SELECT
            variable_name,
            variable_value
        FROM performance_schema.global_status
        WHERE variable_name IN (
            'Innodb_buffer_pool_reads',
            'Innodb_buffer_pool_read_requests',
            'Qcache_hits',
            'Qcache_inserts'
        )
        """

    def get_index_usage_query(self) -> str:
        return """
        SELECT
            object_schema as schema_name,
            object_name as table_name,
            index_name,
            count_read,
            count_insert,
            count_update,
            count_delete
        FROM performance_schema.table_io_waits_summary_by_index_usage
        WHERE object_schema NOT IN ('mysql', 'information_schema', 'performance_schema', 'sys')
        ORDER BY count_read DESC
        LIMIT 10
        """

    def get_configuration_query(self, param_name: str = None) -> str:
        if param_name:
            return f"SHOW VARIABLES LIKE '{param_name}'"
        return "SHOW VARIABLES"

    def get_connection_args(self) -> Dict:
        return {
            "charset": "utf8mb4",
            "connect_timeout": 10,
        }


class PostgreSQLDialect(DatabaseDialect):
    """PostgreSQL-specific SQL dialect"""

    def __init__(self):
        super().__init__()
        self.db_type = DatabaseType.POSTGRESQL

    def get_database_size_query(self) -> str:
        return """
        SELECT
            schemaname as schema_name,
            ROUND(SUM(pg_total_relation_size(schemaname||'.'||tablename)) / 1024 / 1024, 2) as size_mb
        FROM pg_tables
        WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
        GROUP BY schemaname
        ORDER BY size_mb DESC
        """

    def get_slow_queries_query(self, limit: int = 10) -> str:
        return f"""
        SELECT
            query as query,
            calls as execution_count,
            ROUND(mean_exec_time::numeric, 2) as avg_time_ms,
            ROUND(max_exec_time::numeric, 2) as max_time_ms
        FROM pg_stat_statements
        WHERE query NOT LIKE '%pg_stat%'
        ORDER BY total_exec_time DESC
        LIMIT {limit}
        """

    def get_table_statistics_query(self) -> str:
        return """
        SELECT
            schemaname as schema_name,
            tablename as table_name,
            ROUND(pg_total_relation_size(schemaname||'.'||tablename) / 1024.0 / 1024.0, 2) as size_mb,
            n_live_tup as row_count
        FROM pg_stat_user_tables
        ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
        """

    def get_process_list_query(self) -> str:
        return """
        SELECT
            pid,
            usename as user,
            client_addr as client,
            datname as database_name,
            state,
            EXTRACT(EPOCH FROM (now() - query_start))::int as duration_sec,
            LEFT(query, 100) as query
        FROM pg_stat_activity
        WHERE state != 'idle'
        ORDER BY query_start
        """

    def get_lock_info_query(self) -> str:
        return """
        SELECT
            waiting_pid,
            waiting_query,
            blocking_pid,
            blocking_query
        FROM pg_blocking_pids() as blocked_pids
        """

    def get_error_log_query(self) -> str:
        return """
        SELECT
            'pg_log_entries' as metric,
            COUNT(*) as value
        FROM pg_catalog.pg_stat_activity
        WHERE state_change < NOW() - INTERVAL '1 hour'
        """

    def get_cache_efficiency_query(self) -> str:
        return """
        SELECT
            'cache_hit_ratio' as metric,
            ROUND(
                SUM(heap_blks_hit) / (SUM(heap_blks_hit) + SUM(heap_blks_read)) * 100, 2
            ) as value
        FROM pg_statio_user_tables
        """

    def get_index_usage_query(self) -> str:
        return """
        SELECT
            schemaname as schema_name,
            tablename as table_name,
            indexname as index_name,
            idx_scan as scan_count,
            idx_tup_read as tuple_read,
            idx_tup_fetch as tuple_fetch
        FROM pg_stat_user_indexes
        ORDER BY idx_scan DESC
        LIMIT 10
        """

    def get_configuration_query(self, param_name: str = None) -> str:
        if param_name:
            return f"SHOW {param_name}"
        return "SHOW ALL"

    def get_connection_args(self) -> Dict:
        return {
            "connect_timeout": 10,
        }


class InformixDialect(DatabaseDialect):
    """Informix-specific SQL dialect"""

    def __init__(self):
        super().__init__()
        self.db_type = DatabaseType.INFORMIX

    def get_database_size_query(self) -> str:
        return """
        SELECT
            dbsname as schema_name,
            ROUND(SUM(size * 2048.0 / 1024 / 1024), 2) as size_mb
        FROM systables t
        JOIN sysdbstab d ON t.dbsid = d.dbsid
        WHERE dbsname NOT IN ('sysutils', 'syscat')
        GROUP BY dbsname
        ORDER BY size_mb DESC
        """

    def get_slow_queries_query(self, limit: int = 10) -> str:
        return f"""
        SELECT
            tabname as query,
            COUNT(*) as execution_count,
            0 as avg_time_sec,
            0 as max_time_sec
        FROM syscat.tables
        LIMIT {limit}
        """

    def get_table_statistics_query(self) -> str:
        return """
        SELECT
            trim(dbsname) as schema_name,
            trim(tabname) as table_name,
            ROUND((size * 2048.0 / 1024 / 1024), 2) as size_mb,
            nrows as row_count
        FROM systables
        WHERE dbsid != 1
        ORDER BY size DESC
        """

    def get_process_list_query(self) -> str:
        return """
        SELECT
            sid as session_id,
            user_name as user,
            hostname as host,
            dbname as database_name,
            'ACTIVE' as state,
            0 as duration_sec,
            '' as query
        FROM sysadmin:ph_stat
        """

    def get_lock_info_query(self) -> str:
        return """
        SELECT
            waitstmt as waiting_query,
            '' as blocking_query
        FROM sysadmin:locks
        WHERE type = 'W'
        """

    def get_error_log_query(self) -> str:
        return """
        SELECT
            'error_count' as metric,
            COUNT(*) as value
        FROM informix.syserrors
        """

    def get_cache_efficiency_query(self) -> str:
        return """
        SELECT
            'buffer_pool' as metric,
            buffhit as value
        FROM sysadmin:onstat_m
        """

    def get_index_usage_query(self) -> str:
        return """
        SELECT
            trim(dbsname) as schema_name,
            trim(tabname) as table_name,
            trim(idxname) as index_name,
            0 as scan_count,
            0 as tuple_read,
            0 as tuple_fetch
        FROM sysindexes
        LIMIT 10
        """

    def get_configuration_query(self, param_name: str = None) -> str:
        return "ONSTAT -c"

    def get_connection_args(self) -> Dict:
        return {
            "connect_timeout": 10,
        }


# Database dialect registry
DIALECT_REGISTRY: Dict[DatabaseType, DatabaseDialect] = {
    DatabaseType.MYSQL: MySQLDialect(),
    DatabaseType.POSTGRESQL: PostgreSQLDialect(),
    DatabaseType.INFORMIX: InformixDialect(),
}


def get_dialect(db_type: DatabaseType) -> DatabaseDialect:
    """Get dialect for database type"""
    if db_type not in DIALECT_REGISTRY:
        raise ValueError(f"Unsupported database type: {db_type}")
    return DIALECT_REGISTRY[db_type]


def detect_database_type(dsn: str) -> DatabaseType:
    """Detect database type from DSN/connection string"""
    dsn_lower = dsn.lower()

    if "mysql" in dsn_lower or "pymysql" in dsn_lower:
        return DatabaseType.MYSQL
    elif "postgres" in dsn_lower or "psycopg" in dsn_lower:
        return DatabaseType.POSTGRESQL
    elif "informix" in dsn_lower:
        return DatabaseType.INFORMIX
    elif "mariadb" in dsn_lower:
        return DatabaseType.MARIADB
    else:
        raise ValueError(f"Could not detect database type from DSN: {dsn}")
