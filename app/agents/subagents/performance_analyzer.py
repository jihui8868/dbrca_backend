"""Performance analysis sub-agent for MySQL diagnosis"""
from typing import Dict, List, Any
from app.core.database import db_manager


class PerformanceAnalyzer:
    """Analyzes MySQL performance metrics"""

    def __init__(self):
        self.name = "Performance Analyzer"
        self.description = "Analyzes database performance metrics including slow queries, resource usage"

    def analyze(self) -> Dict[str, Any]:
        """Perform performance analysis"""
        return {
            "slow_queries": self._get_slow_queries(),
            "connection_info": self._get_connection_info(),
            "cache_efficiency": self._get_cache_efficiency(),
            "disk_io": self._get_disk_io_info(),
        }

    def _get_slow_queries(self) -> Dict[str, Any]:
        """Analyze slow queries"""
        try:
            slow_queries = db_manager.get_slow_queries(limit=10)
            if not slow_queries:
                return {"status": "ok", "message": "No slow queries detected"}

            return {
                "status": "warning",
                "count": len(slow_queries),
                "queries": slow_queries,
                "recommendation": "Review and optimize the identified slow queries"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _get_connection_info(self) -> Dict[str, Any]:
        """Get connection pool information"""
        try:
            process_list = db_manager.get_process_list()
            active_connections = len(process_list)

            max_connections = db_manager.get_variable("max_connections")
            if max_connections:
                max_connections = int(max_connections)
                utilization = (active_connections / max_connections) * 100
            else:
                utilization = 0

            return {
                "active_connections": active_connections,
                "max_connections": max_connections,
                "utilization_percent": utilization,
                "process_list": process_list
            }
        except Exception as e:
            return {"error": str(e)}

    def _get_cache_efficiency(self) -> Dict[str, Any]:
        """Analyze query cache efficiency"""
        try:
            query = """
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
            results = db_manager.execute_query(query)

            cache_data = {row['variable_name']: int(row['variable_value']) for row in results}

            if 'Innodb_buffer_pool_reads' in cache_data:
                total_reads = (
                    cache_data.get('Innodb_buffer_pool_reads', 0) +
                    cache_data.get('Innodb_buffer_pool_read_requests', 1)
                )
                hit_ratio = (
                    (cache_data.get('Innodb_buffer_pool_read_requests', 0) / total_reads * 100)
                    if total_reads > 0 else 0
                )
                return {
                    "buffer_pool_hit_ratio": f"{hit_ratio:.2f}%",
                    "cache_data": cache_data
                }
            return {"cache_data": cache_data}
        except Exception as e:
            return {"error": str(e)}

    def _get_disk_io_info(self) -> Dict[str, Any]:
        """Get disk I/O information"""
        try:
            query = """
            SELECT
                object_schema,
                object_name,
                count_read,
                count_write,
                count_delete,
                count_update
            FROM performance_schema.table_io_waits_summary_by_table
            WHERE object_schema NOT IN ('mysql', 'information_schema', 'performance_schema', 'sys')
            ORDER BY (count_read + count_write) DESC
            LIMIT 5
            """
            return {
                "top_io_tables": db_manager.execute_query(query)
            }
        except Exception as e:
            return {"error": str(e)}

    def get_summary(self) -> str:
        """Get performance analysis summary"""
        analysis = self.analyze()
        summary = f"Performance Analysis by {self.name}:\n"

        if analysis["slow_queries"].get("status") == "warning":
            summary += f"⚠️  Found {analysis['slow_queries']['count']} slow queries\n"
        else:
            summary += "✓ No slow queries detected\n"

        conn_info = analysis["connection_info"]
        if "utilization_percent" in conn_info:
            summary += f"📊 Connection utilization: {conn_info['utilization_percent']:.1f}%\n"

        return summary
