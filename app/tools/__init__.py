"""Tools for database analysis agents"""

from .performance_tools import (
    PerformanceMetrics,
    get_slow_queries_report,
    get_cache_efficiency_report,
    get_connection_analysis_report,
    get_table_statistics_report,
    get_lock_analysis_report,
    get_disk_io_report,
    get_index_analysis_report,
    get_comprehensive_performance_report,
)

from .log_tools import (
    LogAnalyzer,
    get_error_patterns_report,
    get_connection_issues_report,
    get_warning_events_report,
    get_replication_status_report,
    get_log_volume_report,
    get_event_timeline_report,
    get_comprehensive_log_report,
)

__all__ = [
    # Performance tools
    "PerformanceMetrics",
    "get_slow_queries_report",
    "get_cache_efficiency_report",
    "get_connection_analysis_report",
    "get_table_statistics_report",
    "get_lock_analysis_report",
    "get_disk_io_report",
    "get_index_analysis_report",
    "get_comprehensive_performance_report",
    # Log tools
    "LogAnalyzer",
    "get_error_patterns_report",
    "get_connection_issues_report",
    "get_warning_events_report",
    "get_replication_status_report",
    "get_log_volume_report",
    "get_event_timeline_report",
    "get_comprehensive_log_report",
]
