"""Performance Analysis Tools for Database Diagnostics"""
from typing import Dict, List, Any, Optional
from datetime import datetime
from app.core.database import db_manager


class PerformanceMetrics:
    """Performance metrics analyzer with actionable insights"""

    @staticmethod
    def analyze_slow_queries(limit: int = 10) -> Dict[str, Any]:
        """
        Analyze slow queries and identify patterns

        Args:
            limit: Number of slow queries to analyze

        Returns:
            Dictionary with slow query analysis
        """
        try:
            queries = db_manager.get_slow_queries(limit=limit)

            if not queries:
                return {
                    "status": "OK",
                    "count": 0,
                    "message": "No slow queries detected",
                    "recommendations": []
                }

            # Calculate statistics
            total_queries = len(queries)

            # Analyze patterns
            slow_query_analysis = {
                "status": "WARNING" if total_queries > 5 else "CRITICAL" if total_queries > 20 else "INFO",
                "count": total_queries,
                "queries": queries[:limit],
                "message": f"Found {total_queries} slow queries in recent history",
                "recommendations": [
                    "Review slow query log regularly",
                    "Create indexes on frequently searched columns",
                    "Optimize query execution plans",
                    "Consider query rewriting for complex queries"
                ] if total_queries > 0 else []
            }

            return slow_query_analysis

        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Failed to analyze slow queries: {str(e)}",
                "recommendations": []
            }

    @staticmethod
    def analyze_cache_efficiency() -> Dict[str, Any]:
        """
        Analyze cache efficiency and buffer pool usage

        Returns:
            Dictionary with cache efficiency metrics
        """
        try:
            cache_data = db_manager.get_cache_efficiency()

            if not cache_data:
                return {
                    "status": "UNKNOWN",
                    "message": "Unable to retrieve cache efficiency data",
                    "recommendations": []
                }

            # Extract first result (most relevant metrics)
            metrics = cache_data[0] if cache_data else {}

            # Analyze cache hit ratio if available
            cache_analysis = {
                "status": "OK",
                "metrics": metrics,
                "timestamp": datetime.now().isoformat(),
                "recommendations": []
            }

            # Add recommendations based on metrics
            if "hit_ratio" in metrics or "cache_hit_ratio" in metrics:
                ratio_key = "hit_ratio" if "hit_ratio" in metrics else "cache_hit_ratio"
                ratio = float(str(metrics.get(ratio_key, "0%")).rstrip("%"))

                if ratio < 80:
                    cache_analysis["status"] = "WARNING"
                    cache_analysis["recommendations"].append(
                        f"Cache hit ratio is {ratio}%. Consider increasing innodb_buffer_pool_size"
                    )
                elif ratio < 90:
                    cache_analysis["recommendations"].append(
                        f"Cache hit ratio is {ratio}%. Monitor memory usage"
                    )

            cache_analysis["recommendations"].extend([
                "Monitor cache effectiveness regularly",
                "Adjust buffer pool size based on workload",
                "Identify and optimize high-miss queries"
            ])

            return cache_analysis

        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Failed to analyze cache efficiency: {str(e)}",
                "recommendations": []
            }

    @staticmethod
    def analyze_connections() -> Dict[str, Any]:
        """
        Analyze connection pool usage and health

        Returns:
            Dictionary with connection analysis
        """
        try:
            processes = db_manager.get_process_list()

            if not processes:
                return {
                    "status": "OK",
                    "active_connections": 0,
                    "message": "No active connections",
                    "recommendations": []
                }

            active_count = len(processes)

            # Get max connections configuration
            max_connections_str = db_manager.get_variable("max_connections")
            max_connections = int(max_connections_str) if max_connections_str else 100

            utilization = (active_count / max_connections * 100) if max_connections else 0

            status = "OK"
            if utilization > 90:
                status = "CRITICAL"
            elif utilization > 75:
                status = "WARNING"

            connection_analysis = {
                "status": status,
                "active_connections": active_count,
                "max_connections": max_connections,
                "utilization_percent": round(utilization, 2),
                "connections": processes[:10],  # Top 10 connections
                "message": f"Using {active_count}/{max_connections} connections ({utilization:.1f}%)",
                "recommendations": []
            }

            if status == "CRITICAL":
                connection_analysis["recommendations"].append(
                    f"Connection pool utilization is {utilization:.1f}%. Consider increasing max_connections"
                )
            elif status == "WARNING":
                connection_analysis["recommendations"].append(
                    f"Connection pool utilization is {utilization:.1f}%. Monitor closely"
                )

            connection_analysis["recommendations"].extend([
                "Close idle connections",
                "Use connection pooling",
                "Review long-running queries"
            ])

            return connection_analysis

        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Failed to analyze connections: {str(e)}",
                "recommendations": []
            }

    @staticmethod
    def analyze_table_statistics() -> Dict[str, Any]:
        """
        Analyze table statistics and identify large tables

        Returns:
            Dictionary with table analysis
        """
        try:
            tables = db_manager.get_table_statistics()

            if not tables:
                return {
                    "status": "OK",
                    "table_count": 0,
                    "message": "No tables found",
                    "recommendations": []
                }

            # Sort by size (largest first)
            sorted_tables = sorted(
                tables,
                key=lambda x: float(str(x.get("size", "0")).replace("MB", "").strip() or "0"),
                reverse=True
            )

            total_tables = len(tables)
            largest_tables = sorted_tables[:5]

            table_analysis = {
                "status": "OK",
                "table_count": total_tables,
                "largest_tables": largest_tables,
                "all_tables": tables,
                "message": f"Database contains {total_tables} tables",
                "recommendations": []
            }

            # Add recommendations for large tables
            if largest_tables:
                table_analysis["recommendations"].extend([
                    "Consider partitioning large tables",
                    "Review index usage on large tables",
                    "Implement archival strategy for old data",
                    "Monitor table growth trends"
                ])

            return table_analysis

        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Failed to analyze table statistics: {str(e)}",
                "recommendations": []
            }

    @staticmethod
    def analyze_locks() -> Dict[str, Any]:
        """
        Analyze lock information and contention

        Returns:
            Dictionary with lock analysis
        """
        try:
            locks = db_manager.get_lock_info()

            if not locks:
                return {
                    "status": "OK",
                    "lock_count": 0,
                    "message": "No locks detected",
                    "recommendations": []
                }

            lock_analysis = {
                "status": "WARNING" if len(locks) > 5 else "OK",
                "lock_count": len(locks),
                "locks": locks,
                "message": f"Found {len(locks)} active locks",
                "recommendations": []
            }

            if len(locks) > 5:
                lock_analysis["recommendations"].extend([
                    "Lock contention detected",
                    "Review long-running transactions",
                    "Optimize query execution order",
                    "Consider increasing isolation level or using row locks"
                ])
            else:
                lock_analysis["recommendations"].extend([
                    "Monitor lock patterns",
                    "Review deadlock events",
                    "Optimize transaction boundaries"
                ])

            return lock_analysis

        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Failed to analyze locks: {str(e)}",
                "recommendations": []
            }

    @staticmethod
    def analyze_disk_io() -> Dict[str, Any]:
        """
        Analyze disk I/O patterns and performance

        Returns:
            Dictionary with disk I/O analysis
        """
        try:
            # Get database size as proxy for I/O volume
            db_size = db_manager.get_database_size()

            if not db_size:
                return {
                    "status": "UNKNOWN",
                    "message": "Unable to retrieve disk I/O data",
                    "recommendations": []
                }

            disk_analysis = {
                "status": "OK",
                "database_size": db_size,
                "message": f"Database size: {db_size[0].get('size', 'unknown')}",
                "recommendations": []
            }

            # Add I/O optimization recommendations
            disk_analysis["recommendations"].extend([
                "Monitor disk space utilization",
                "Implement SSD for better I/O performance",
                "Archive old data to reduce I/O volume",
                "Optimize query plans to reduce disk reads"
            ])

            return disk_analysis

        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Failed to analyze disk I/O: {str(e)}",
                "recommendations": []
            }

    @staticmethod
    def analyze_indexes() -> Dict[str, Any]:
        """
        Analyze index usage and identify missing indexes

        Returns:
            Dictionary with index analysis
        """
        try:
            index_usage = db_manager.get_index_usage()

            if not index_usage:
                return {
                    "status": "UNKNOWN",
                    "message": "Index usage data not available",
                    "recommendations": []
                }

            # Identify unused indexes
            unused_indexes = [idx for idx in index_usage if idx.get("usage_count", 0) == 0]

            index_analysis = {
                "status": "OK" if not unused_indexes else "WARNING",
                "total_indexes": len(index_usage),
                "unused_indexes": len(unused_indexes),
                "index_data": index_usage,
                "message": f"Total indexes: {len(index_usage)}, Unused: {len(unused_indexes)}",
                "recommendations": []
            }

            if unused_indexes:
                index_analysis["recommendations"].extend([
                    f"Found {len(unused_indexes)} unused indexes - consider dropping them",
                    "Unused indexes consume memory and slow down writes",
                    "Review index strategy for frequently accessed tables"
                ])

            index_analysis["recommendations"].extend([
                "Monitor index effectiveness",
                "Add indexes for slow queries",
                "Review index fragmentation regularly"
            ])

            return index_analysis

        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Failed to analyze indexes: {str(e)}",
                "recommendations": []
            }

    @staticmethod
    def generate_performance_report() -> Dict[str, Any]:
        """
        Generate comprehensive performance analysis report

        Returns:
            Complete performance analysis report
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "database_info": db_manager.get_database_info(),
            "analyses": {
                "slow_queries": PerformanceMetrics.analyze_slow_queries(),
                "cache_efficiency": PerformanceMetrics.analyze_cache_efficiency(),
                "connections": PerformanceMetrics.analyze_connections(),
                "table_statistics": PerformanceMetrics.analyze_table_statistics(),
                "locks": PerformanceMetrics.analyze_locks(),
                "disk_io": PerformanceMetrics.analyze_disk_io(),
                "indexes": PerformanceMetrics.analyze_indexes(),
            },
            "overall_status": "OK",
            "critical_issues": [],
            "recommendations": []
        }

        # Determine overall status and collect issues
        for analysis_name, analysis_result in report["analyses"].items():
            status = analysis_result.get("status", "UNKNOWN")

            if status == "CRITICAL":
                report["overall_status"] = "CRITICAL"
                report["critical_issues"].append(analysis_name)
            elif status == "WARNING" and report["overall_status"] != "CRITICAL":
                report["overall_status"] = "WARNING"

            # Collect recommendations
            recommendations = analysis_result.get("recommendations", [])
            if recommendations:
                report["recommendations"].extend(recommendations)

        return report


# Convenience functions for use as tools
def get_slow_queries_report(limit: int = 10) -> str:
    """Get slow queries analysis report"""
    result = PerformanceMetrics.analyze_slow_queries(limit)
    return f"Status: {result.get('status')}\n{result.get('message')}\nRecommendations: {', '.join(result.get('recommendations', []))}"


def get_cache_efficiency_report() -> str:
    """Get cache efficiency analysis report"""
    result = PerformanceMetrics.analyze_cache_efficiency()
    return f"Status: {result.get('status')}\n{result.get('message')}\nMetrics: {result.get('metrics')}"


def get_connection_analysis_report() -> str:
    """Get connection pool analysis report"""
    result = PerformanceMetrics.analyze_connections()
    return f"Status: {result.get('status')}\nConnections: {result.get('active_connections')}/{result.get('max_connections')} ({result.get('utilization_percent')}%)"


def get_table_statistics_report() -> str:
    """Get table statistics analysis report"""
    result = PerformanceMetrics.analyze_table_statistics()
    return f"Status: {result.get('status')}\nTables: {result.get('table_count')}\nLargest Tables: {[t.get('table_name') for t in result.get('largest_tables', [])]}"


def get_lock_analysis_report() -> str:
    """Get lock analysis report"""
    result = PerformanceMetrics.analyze_locks()
    return f"Status: {result.get('status')}\nLocks: {result.get('lock_count')}\nMessage: {result.get('message')}"


def get_disk_io_report() -> str:
    """Get disk I/O analysis report"""
    result = PerformanceMetrics.analyze_disk_io()
    return f"Status: {result.get('status')}\nMessage: {result.get('message')}"


def get_index_analysis_report() -> str:
    """Get index analysis report"""
    result = PerformanceMetrics.analyze_indexes()
    return f"Status: {result.get('status')}\nTotal Indexes: {result.get('total_indexes')}\nUnused Indexes: {result.get('unused_indexes')}"


def get_comprehensive_performance_report() -> str:
    """Get comprehensive performance analysis report"""
    report = PerformanceMetrics.generate_performance_report()

    summary = f"""
COMPREHENSIVE PERFORMANCE ANALYSIS REPORT
==========================================
Timestamp: {report['timestamp']}
Database: {report['database_info'].get('type')}
Overall Status: {report['overall_status']}

Critical Issues: {', '.join(report['critical_issues']) if report['critical_issues'] else 'None'}

Top Recommendations:
{chr(10).join([f"• {rec}" for rec in report['recommendations'][:5]])}

Detailed Findings:
- Slow Queries: {report['analyses']['slow_queries'].get('status')}
- Cache Efficiency: {report['analyses']['cache_efficiency'].get('status')}
- Connections: {report['analyses']['connections'].get('status')}
- Tables: {report['analyses']['table_statistics'].get('status')}
- Locks: {report['analyses']['locks'].get('status')}
- Disk I/O: {report['analyses']['disk_io'].get('status')}
- Indexes: {report['analyses']['indexes'].get('status')}
"""

    return summary.strip()
