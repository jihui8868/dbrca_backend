"""Log Analysis Tools for Database Diagnostics"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from app.core.database import db_manager


class LogAnalyzer:
    """Log analysis tools for database diagnostics"""

    @staticmethod
    def analyze_error_patterns(hours: int = 24) -> Dict[str, Any]:
        """
        Analyze error patterns from database logs

        Args:
            hours: Hours of log history to analyze

        Returns:
            Dictionary with error pattern analysis
        """
        try:
            logs = db_manager.get_error_log()

            if not logs:
                return {
                    "status": "OK",
                    "message": "No errors detected in log",
                    "error_count": 0,
                    "recommendations": []
                }

            # Group errors by type
            error_types = {}
            for log in logs:
                error_msg = log.get("message", "Unknown").split(":")[0]
                if error_msg not in error_types:
                    error_types[error_msg] = 0
                error_types[error_msg] += 1

            # Sort by frequency
            top_errors = sorted(error_types.items(), key=lambda x: x[1], reverse=True)[:10]

            status = "OK"
            if len(logs) > 10:
                status = "WARNING"
            if len(logs) > 50:
                status = "CRITICAL"

            error_analysis = {
                "status": status,
                "message": f"Found {len(logs)} errors in recent logs",
                "error_count": len(logs),
                "top_error_patterns": [
                    {"error": error, "count": count} for error, count in top_errors
                ],
                "recommendations": []
            }

            if status == "CRITICAL":
                error_analysis["recommendations"].extend([
                    f"Critical: {len(logs)} errors detected - investigate immediately",
                    "Review recent application changes",
                    "Check resource availability (disk, memory, connections)"
                ])
            elif status == "WARNING":
                error_analysis["recommendations"].extend([
                    f"Warning: {len(logs)} errors found - monitor closely",
                    "Analyze most frequent error patterns",
                    "Review application logs for context"
                ])

            return error_analysis

        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Failed to analyze error patterns: {str(e)}",
                "error_count": 0,
                "recommendations": []
            }

    @staticmethod
    def analyze_connection_issues() -> Dict[str, Any]:
        """
        Analyze connection-related issues from logs

        Returns:
            Dictionary with connection issue analysis
        """
        try:
            logs = db_manager.get_error_log()

            if not logs:
                return {
                    "status": "OK",
                    "message": "No connection issues detected",
                    "aborted_connections": 0,
                    "recommendations": []
                }

            # Count connection-related errors
            connection_errors = [
                log for log in logs
                if "connection" in log.get("message", "").lower() or
                   "host" in log.get("message", "").lower()
            ]

            aborted_count = len(connection_errors)

            status = "OK"
            if aborted_count > 5:
                status = "WARNING"
            if aborted_count > 20:
                status = "CRITICAL"

            connection_analysis = {
                "status": status,
                "message": f"Found {aborted_count} connection-related issues",
                "aborted_connections": aborted_count,
                "connection_errors": connection_errors[:5],
                "recommendations": []
            }

            if status == "CRITICAL":
                connection_analysis["recommendations"].extend([
                    "High connection failure rate detected",
                    "Check network connectivity and firewall rules",
                    "Review max_connections and timeout settings",
                    "Monitor application connection pooling"
                ])
            elif status == "WARNING":
                connection_analysis["recommendations"].extend([
                    "Connection issues detected - review settings",
                    "Check application authentication logic",
                    "Monitor connection pool health"
                ])

            return connection_analysis

        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Failed to analyze connection issues: {str(e)}",
                "aborted_connections": 0,
                "recommendations": []
            }

    @staticmethod
    def analyze_warning_events() -> Dict[str, Any]:
        """
        Analyze warning events from database logs

        Returns:
            Dictionary with warning event analysis
        """
        try:
            logs = db_manager.get_error_log()

            if not logs:
                return {
                    "status": "OK",
                    "message": "No warning events detected",
                    "warning_count": 0,
                    "recommendations": []
                }

            # Count warning-level events
            warnings = [
                log for log in logs
                if "warning" in str(log.get("level", "")).lower() or
                   "warn" in log.get("message", "").lower()
            ]

            warning_count = len(warnings)

            status = "OK"
            if warning_count > 5:
                status = "WARNING"
            if warning_count > 20:
                status = "CRITICAL"

            warning_analysis = {
                "status": status,
                "message": f"Found {warning_count} warning events",
                "warning_count": warning_count,
                "warnings": warnings[:10],
                "recommendations": []
            }

            if warning_count > 0:
                warning_analysis["recommendations"].extend([
                    "Review warning messages for patterns",
                    "Address deprecated feature warnings",
                    "Monitor resource-related warnings"
                ])

            return warning_analysis

        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Failed to analyze warning events: {str(e)}",
                "warning_count": 0,
                "recommendations": []
            }

    @staticmethod
    def analyze_replication_status() -> Dict[str, Any]:
        """
        Analyze replication-related issues from logs

        Returns:
            Dictionary with replication status analysis
        """
        try:
            logs = db_manager.get_error_log()

            if not logs:
                return {
                    "status": "OK",
                    "message": "Replication status: healthy",
                    "replication_issues": 0,
                    "recommendations": []
                }

            # Count replication-related errors
            replication_errors = [
                log for log in logs
                if any(keyword in log.get("message", "").lower()
                       for keyword in ["replicas", "replication", "binlog", "slave", "relay"])
            ]

            issue_count = len(replication_errors)

            status = "OK"
            if issue_count > 0:
                status = "WARNING"
            if issue_count > 5:
                status = "CRITICAL"

            replication_analysis = {
                "status": status,
                "message": f"Replication issues: {issue_count}" if issue_count > 0 else "Replication status: healthy",
                "replication_issues": issue_count,
                "issues": replication_errors[:5],
                "recommendations": []
            }

            if status != "OK":
                replication_analysis["recommendations"].extend([
                    "Review replication error log for details",
                    "Check slave thread status and positions",
                    "Verify network connectivity between primary and replica",
                    "Consider running SHOW SLAVE STATUS for detailed info"
                ])

            return replication_analysis

        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Failed to analyze replication status: {str(e)}",
                "replication_issues": 0,
                "recommendations": []
            }

    @staticmethod
    def analyze_log_volume() -> Dict[str, Any]:
        """
        Analyze log volume and growth patterns

        Returns:
            Dictionary with log volume analysis
        """
        try:
            logs = db_manager.get_error_log()

            if not logs:
                return {
                    "status": "OK",
                    "message": "Log volume: normal",
                    "total_entries": 0,
                    "recommendations": []
                }

            total_entries = len(logs)

            status = "OK"
            if total_entries > 100:
                status = "WARNING"
            if total_entries > 500:
                status = "CRITICAL"

            # Count entries by level if available
            level_counts = {}
            for log in logs:
                level = log.get("level", "INFO")
                level_counts[level] = level_counts.get(level, 0) + 1

            volume_analysis = {
                "status": status,
                "message": f"Total log entries: {total_entries}",
                "total_entries": total_entries,
                "entries_by_level": level_counts,
                "recommendations": []
            }

            if status == "CRITICAL":
                volume_analysis["recommendations"].extend([
                    "High log volume detected",
                    "Implement log rotation if not already enabled",
                    "Archive old logs to reduce disk usage",
                    "Review and optimize verbose logging settings"
                ])
            elif status == "WARNING":
                volume_analysis["recommendations"].extend([
                    "Monitor log growth rate",
                    "Configure log rotation with appropriate retention",
                    "Consider reducing log verbosity for noisy components"
                ])

            return volume_analysis

        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Failed to analyze log volume: {str(e)}",
                "total_entries": 0,
                "recommendations": []
            }

    @staticmethod
    def analyze_event_timeline() -> Dict[str, Any]:
        """
        Analyze event timeline and patterns in logs

        Returns:
            Dictionary with event timeline analysis
        """
        try:
            logs = db_manager.get_error_log()

            if not logs:
                return {
                    "status": "OK",
                    "message": "No unusual event patterns detected",
                    "event_count": 0,
                    "recommendations": []
                }

            # Analyze temporal distribution
            event_count = len(logs)

            # Group by type of event
            event_types = {}
            for log in logs:
                msg = log.get("message", "Unknown")
                if "error" in msg.lower():
                    event_type = "Error"
                elif "warning" in msg.lower():
                    event_type = "Warning"
                else:
                    event_type = "Event"

                event_types[event_type] = event_types.get(event_type, 0) + 1

            status = "OK"
            if event_count > 20:
                status = "WARNING"
            if event_count > 100:
                status = "CRITICAL"

            timeline_analysis = {
                "status": status,
                "message": f"Timeline analysis: {event_count} events detected",
                "event_count": event_count,
                "event_distribution": event_types,
                "latest_events": logs[:5] if logs else [],
                "recommendations": []
            }

            if status == "CRITICAL":
                timeline_analysis["recommendations"].extend([
                    "Multiple clustered events detected",
                    "Review events around the same timeframe",
                    "Correlate with system metrics (CPU, disk, memory)"
                ])
            elif status == "WARNING":
                timeline_analysis["recommendations"].extend([
                    "Monitor event patterns over time",
                    "Identify recurring issues",
                    "Track event frequency trends"
                ])

            return timeline_analysis

        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Failed to analyze event timeline: {str(e)}",
                "event_count": 0,
                "recommendations": []
            }

    @staticmethod
    def generate_log_report() -> Dict[str, Any]:
        """
        Generate comprehensive log analysis report

        Returns:
            Complete log analysis report
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "database_info": db_manager.get_database_info(),
            "analyses": {
                "error_patterns": LogAnalyzer.analyze_error_patterns(),
                "connection_issues": LogAnalyzer.analyze_connection_issues(),
                "warning_events": LogAnalyzer.analyze_warning_events(),
                "replication_status": LogAnalyzer.analyze_replication_status(),
                "log_volume": LogAnalyzer.analyze_log_volume(),
                "event_timeline": LogAnalyzer.analyze_event_timeline(),
            },
            "overall_status": "OK",
            "critical_issues": [],
            "recommendations": []
        }

        # Determine overall status
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
def get_error_patterns_report(hours: int = 24) -> str:
    """Get error pattern analysis report"""
    result = LogAnalyzer.analyze_error_patterns(hours)
    return f"Status: {result.get('status')}\n{result.get('message')}\nTop Errors: {[e['error'] for e in result.get('top_error_patterns', [])]}\nRecommendations: {', '.join(result.get('recommendations', []))}"


def get_connection_issues_report() -> str:
    """Get connection issues analysis report"""
    result = LogAnalyzer.analyze_connection_issues()
    return f"Status: {result.get('status')}\nAborted Connections: {result.get('aborted_connections')}\nMessage: {result.get('message')}"


def get_warning_events_report() -> str:
    """Get warning events analysis report"""
    result = LogAnalyzer.analyze_warning_events()
    return f"Status: {result.get('status')}\nWarning Count: {result.get('warning_count')}\nMessage: {result.get('message')}"


def get_replication_status_report() -> str:
    """Get replication status analysis report"""
    result = LogAnalyzer.analyze_replication_status()
    return f"Status: {result.get('status')}\nReplication Issues: {result.get('replication_issues')}\nMessage: {result.get('message')}"


def get_log_volume_report() -> str:
    """Get log volume analysis report"""
    result = LogAnalyzer.analyze_log_volume()
    return f"Status: {result.get('status')}\nTotal Entries: {result.get('total_entries')}\nMessage: {result.get('message')}"


def get_event_timeline_report() -> str:
    """Get event timeline analysis report"""
    result = LogAnalyzer.analyze_event_timeline()
    return f"Status: {result.get('status')}\nEvent Count: {result.get('event_count')}\nDistribution: {result.get('event_distribution')}"


def get_comprehensive_log_report() -> str:
    """Get comprehensive log analysis report"""
    report = LogAnalyzer.generate_log_report()

    summary = f"""
COMPREHENSIVE LOG ANALYSIS REPORT
==================================
Timestamp: {report['timestamp']}
Database: {report['database_info'].get('type')}
Overall Status: {report['overall_status']}

Critical Issues: {', '.join(report['critical_issues']) if report['critical_issues'] else 'None'}

Top Recommendations:
{chr(10).join([f"• {rec}" for rec in report['recommendations'][:5]])}

Detailed Findings:
- Error Patterns: {report['analyses']['error_patterns'].get('status')}
- Connection Issues: {report['analyses']['connection_issues'].get('status')}
- Warning Events: {report['analyses']['warning_events'].get('status')}
- Replication Status: {report['analyses']['replication_status'].get('status')}
- Log Volume: {report['analyses']['log_volume'].get('status')}
- Event Timeline: {report['analyses']['event_timeline'].get('status')}
"""

    return summary.strip()
