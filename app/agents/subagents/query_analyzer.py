"""Query analysis sub-agent for MySQL diagnosis"""
from typing import Dict, Any, List
from app.core.database import db_manager


class QueryAnalyzer:
    """Analyzes query execution patterns and inefficiencies"""

    def __init__(self):
        self.name = "Query Analyzer"
        self.description = "Analyzes query patterns, execution plans, and optimization opportunities"

    def analyze(self) -> Dict[str, Any]:
        """Perform query analysis"""
        return {
            "slow_query_analysis": self._analyze_slow_queries(),
            "table_statistics": self._get_table_statistics(),
            "index_usage": self._analyze_index_usage(),
            "lock_analysis": self._analyze_locks(),
        }

    def _analyze_slow_queries(self) -> Dict[str, Any]:
        """Analyze slow query patterns"""
        try:
            slow_queries = db_manager.get_slow_queries(limit=5)

            if not slow_queries:
                return {"status": "ok", "message": "No slow queries found"}

            analysis = []
            for query in slow_queries:
                analysis.append({
                    "query": query.get("digest_text", "N/A")[:200],
                    "count": query.get("count_star", 0),
                    "avg_time_sec": query.get("avg_time_sec", 0),
                    "max_time_sec": query.get("max_time_sec", 0),
                    "optimization_tips": self._get_optimization_tips(query.get("digest_text", ""))
                })

            return {
                "status": "warning",
                "count": len(slow_queries),
                "queries": analysis
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _get_optimization_tips(self, query_text: str) -> List[str]:
        """Get optimization tips based on query pattern"""
        tips = []

        if "SELECT *" in query_text.upper():
            tips.append("Avoid SELECT * - specify only needed columns")

        if "JOIN" in query_text.upper() and "ON" in query_text.upper():
            tips.append("Verify JOIN columns are properly indexed")

        if "LIKE '%" in query_text.upper():
            tips.append("Leading wildcard patterns cannot use indexes effectively")

        if "OR" in query_text.upper():
            tips.append("Consider using IN clause or UNION for OR conditions")

        if "FUNCTION(" in query_text.upper():
            tips.append("Avoid using functions on indexed columns in WHERE clause")

        if not tips:
            tips.append("Review execution plan with EXPLAIN")

        return tips[:3]

    def _get_table_statistics(self) -> Dict[str, Any]:
        """Get table statistics and fragmentation info"""
        try:
            stats = db_manager.get_table_statistics()

            if not stats:
                return {"status": "ok", "message": "No tables found"}

            large_tables = sorted(stats, key=lambda x: float(x.get("size_mb", 0)), reverse=True)[:5]
            fragmented_tables = [t for t in stats if float(t.get("free_mb", 0)) > float(t.get("size_mb", 0)) * 0.1]

            return {
                "total_tables": len(stats),
                "large_tables": large_tables,
                "fragmented_count": len(fragmented_tables),
                "fragmented_tables": fragmented_tables[:3]
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _analyze_index_usage(self) -> Dict[str, Any]:
        """Analyze index usage patterns"""
        try:
            query = """
            SELECT
                object_schema,
                object_name,
                index_name,
                count_read,
                count_insert,
                count_update,
                count_delete
            FROM performance_schema.table_io_waits_summary_by_index_usage
            WHERE object_schema NOT IN ('mysql', 'information_schema', 'performance_schema', 'sys')
            AND index_name != 'PRIMARY'
            ORDER BY count_read DESC
            LIMIT 10
            """
            index_stats = db_manager.execute_query(query)

            unused_query = """
            SELECT
                object_schema,
                object_name,
                index_name
            FROM performance_schema.table_io_waits_summary_by_index_usage
            WHERE object_schema NOT IN ('mysql', 'information_schema', 'performance_schema', 'sys')
            AND index_name != 'PRIMARY'
            AND count_read = 0
            AND count_insert = 0
            AND count_update = 0
            AND count_delete = 0
            """
            unused_indexes = db_manager.execute_query(unused_query)

            return {
                "total_used_indexes": len(index_stats),
                "top_indexes": index_stats[:5],
                "unused_indexes_count": len(unused_indexes),
                "unused_indexes": unused_indexes[:5]
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _analyze_locks(self) -> Dict[str, Any]:
        """Analyze lock contention"""
        try:
            lock_info = db_manager.get_lock_info()

            if not lock_info:
                return {"status": "ok", "message": "No active locks detected"}

            return {
                "status": "warning",
                "lock_count": len(lock_info),
                "locks": lock_info,
                "recommendation": "Review blocking queries and optimize transaction scope"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_summary(self) -> str:
        """Get query analysis summary"""
        analysis = self.analyze()
        summary = f"Query Analysis by {self.name}:\n"

        slow_query_info = analysis["slow_query_analysis"]
        if slow_query_info.get("status") == "warning":
            summary += f"⚠️  Found {slow_query_info['count']} slow queries\n"
        else:
            summary += "✓ No slow queries detected\n"

        table_stats = analysis["table_statistics"]
        if table_stats.get("fragmented_count", 0) > 0:
            summary += f"📊 {table_stats['fragmented_count']} tables are fragmented\n"

        index_stats = analysis["index_usage"]
        if index_stats.get("unused_indexes_count", 0) > 0:
            summary += f"🔍 {index_stats['unused_indexes_count']} unused indexes found\n"

        lock_info = analysis["lock_analysis"]
        if lock_info.get("status") == "warning":
            summary += f"🔒 {lock_info['lock_count']} lock contentions detected\n"

        return summary
