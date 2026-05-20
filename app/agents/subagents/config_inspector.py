"""Configuration inspection sub-agent for MySQL diagnosis"""
from typing import Dict, Any, List
from app.core.database import db_manager


class ConfigInspector:
    """Inspects MySQL configuration and settings"""

    def __init__(self):
        self.name = "Configuration Inspector"
        self.description = "Analyzes MySQL configuration, system variables, and settings optimization"

    def analyze(self) -> Dict[str, Any]:
        """Perform configuration analysis"""
        return {
            "memory_settings": self._check_memory_settings(),
            "connection_settings": self._check_connection_settings(),
            "logging_config": self._check_logging_config(),
            "innodb_settings": self._check_innodb_settings(),
        }

    def _check_memory_settings(self) -> Dict[str, Any]:
        """Check memory-related settings"""
        try:
            variables = {
                "max_connections": 0,
                "innodb_buffer_pool_size": 0,
                "query_cache_size": 0,
                "sort_buffer_size": 0,
                "read_buffer_size": 0,
            }

            issues = []
            for var_name in variables:
                value = db_manager.get_variable(var_name)
                if value:
                    variables[var_name] = value

            buffer_pool = db_manager.get_variable("innodb_buffer_pool_size")
            if buffer_pool and self._convert_to_bytes(buffer_pool) < 268435456:  # < 256MB
                issues.append("innodb_buffer_pool_size is too small (< 256MB)")

            sort_buffer = db_manager.get_variable("sort_buffer_size")
            if sort_buffer and self._convert_to_bytes(sort_buffer) > 4194304:  # > 4MB
                issues.append("sort_buffer_size is too large (> 4MB)")

            return {
                "variables": variables,
                "issues": issues,
                "status": "warning" if issues else "ok"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _check_connection_settings(self) -> Dict[str, Any]:
        """Check connection configuration"""
        try:
            max_connections = db_manager.get_variable("max_connections")
            max_allowed_packet = db_manager.get_variable("max_allowed_packet")
            connect_timeout = db_manager.get_variable("connect_timeout")
            wait_timeout = db_manager.get_variable("wait_timeout")
            interactive_timeout = db_manager.get_variable("interactive_timeout")

            return {
                "max_connections": max_connections,
                "max_allowed_packet": max_allowed_packet,
                "connect_timeout": connect_timeout,
                "wait_timeout": wait_timeout,
                "interactive_timeout": interactive_timeout,
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _check_logging_config(self) -> Dict[str, Any]:
        """Check logging configuration"""
        try:
            variables = {
                "slow_query_log": db_manager.get_variable("slow_query_log"),
                "long_query_time": db_manager.get_variable("long_query_time"),
                "log_queries_not_using_indexes": db_manager.get_variable("log_queries_not_using_indexes"),
                "binlog_format": db_manager.get_variable("binlog_format"),
                "server_id": db_manager.get_variable("server_id"),
            }

            issues = []
            if variables.get("slow_query_log") == "OFF":
                issues.append("slow_query_log is disabled - enable for performance monitoring")

            if variables.get("log_queries_not_using_indexes") == "OFF":
                issues.append("log_queries_not_using_indexes is disabled")

            return {
                "variables": variables,
                "issues": issues,
                "status": "warning" if issues else "ok"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _check_innodb_settings(self) -> Dict[str, Any]:
        """Check InnoDB-specific settings"""
        try:
            variables = {
                "innodb_flush_log_at_trx_commit": db_manager.get_variable("innodb_flush_log_at_trx_commit"),
                "innodb_file_per_table": db_manager.get_variable("innodb_file_per_table"),
                "innodb_flush_method": db_manager.get_variable("innodb_flush_method"),
                "innodb_log_file_size": db_manager.get_variable("innodb_log_file_size"),
                "innodb_autoinc_lock_mode": db_manager.get_variable("innodb_autoinc_lock_mode"),
            }

            issues = []
            flush_setting = variables.get("innodb_flush_log_at_trx_commit")
            if flush_setting == "1":
                issues.append("innodb_flush_log_at_trx_commit=1 may impact performance on high-load systems")

            if variables.get("innodb_file_per_table") == "OFF":
                issues.append("innodb_file_per_table is disabled - consider enabling for table isolation")

            return {
                "variables": variables,
                "issues": issues,
                "status": "warning" if issues else "ok"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def _convert_to_bytes(value: str) -> int:
        """Convert MySQL variable value to bytes"""
        if not value:
            return 0

        multipliers = {
            'K': 1024,
            'M': 1024 ** 2,
            'G': 1024 ** 3,
            'T': 1024 ** 4,
        }

        value = value.upper().strip()
        for suffix, multiplier in multipliers.items():
            if value.endswith(suffix):
                try:
                    return int(value[:-1]) * multiplier
                except ValueError:
                    return 0

        try:
            return int(value)
        except ValueError:
            return 0

    def get_summary(self) -> str:
        """Get configuration analysis summary"""
        analysis = self.analyze()
        summary = f"Configuration Analysis by {self.name}:\n"

        memory = analysis["memory_settings"]
        if memory.get("issues"):
            summary += f"⚠️  Memory issues: {', '.join(memory['issues'][:1])}\n"
        else:
            summary += "✓ Memory settings look good\n"

        logging = analysis["logging_config"]
        if logging.get("issues"):
            summary += f"📋 Logging recommendations: {len(logging['issues'])} issues\n"

        innodb = analysis["innodb_settings"]
        if innodb.get("issues"):
            summary += f"🔧 InnoDB optimizations: {len(innodb['issues'])} recommendations\n"

        return summary
