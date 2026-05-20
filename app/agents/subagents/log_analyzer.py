"""Log analysis sub-agent for MySQL diagnosis"""
from typing import Dict, Any, List
from datetime import datetime, timedelta
from app.core.database import db_manager


class LogAnalyzer:
    """Analyzes MySQL logs and error patterns"""

    def __init__(self):
        self.name = "Log Analyzer"
        self.description = "Analyzes error logs, warnings, and diagnostic patterns"

    def analyze(self) -> Dict[str, Any]:
        """Perform log analysis"""
        return {
            "error_count": self._get_error_count(),
            "common_errors": self._get_common_errors(),
            "warning_events": self._get_warnings(),
            "replication_status": self._get_replication_status(),
        }

    def _get_error_count(self) -> Dict[str, Any]:
        """Get error count from diagnostics"""
        try:
            query = """
            SELECT
                variable_value as error_count
            FROM performance_schema.global_status
            WHERE variable_name = 'Aborted_connects'
            """
            result = db_manager.execute_query(query)
            count = int(result[0]['error_count']) if result else 0

            if count > 100:
                status = "critical"
                message = "High number of aborted connections detected"
            elif count > 10:
                status = "warning"
                message = "Elevated aborted connection count"
            else:
                status = "ok"
                message = "Normal aborted connection count"

            return {
                "status": status,
                "count": count,
                "message": message
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _get_common_errors(self) -> Dict[str, Any]:
        """Identify common error patterns"""
        try:
            query = """
            SELECT
                event_name,
                count_star as error_count
            FROM performance_schema.events_errors_summary_global_by_error
            WHERE count_star > 0
            ORDER BY count_star DESC
            LIMIT 10
            """
            errors = db_manager.execute_query(query)
            return {
                "count": len(errors),
                "top_errors": errors
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _get_warnings(self) -> Dict[str, Any]:
        """Get recent warnings"""
        try:
            warnings = []
            critical_variables = {
                "Aborted_clients": 10,
                "Aborted_connects": 10,
                "Innodb_log_waits": 0,
                "Slave_open_temp_tables": 0,
            }

            for var_name, threshold in critical_variables.items():
                value = db_manager.get_variable(var_name)
                if value and int(value) > threshold:
                    warnings.append({
                        "variable": var_name,
                        "value": int(value),
                        "threshold": threshold,
                        "severity": "warning" if int(value) < threshold * 5 else "critical"
                    })

            return {
                "warning_count": len(warnings),
                "warnings": warnings
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _get_replication_status(self) -> Dict[str, Any]:
        """Check replication health if applicable"""
        try:
            query = "SHOW SLAVE STATUS"
            result = db_manager.execute_query(query)

            if not result:
                return {"status": "not_applicable", "message": "Not a slave server"}

            slave_status = result[0]
            issues = []

            if slave_status.get('Slave_IO_Running') != 'Yes':
                issues.append("Slave IO thread is not running")
            if slave_status.get('Slave_SQL_Running') != 'Yes':
                issues.append("Slave SQL thread is not running")

            seconds_behind = slave_status.get('Seconds_Behind_Master')
            if seconds_behind and int(seconds_behind) > 60:
                issues.append(f"Replication lag: {seconds_behind} seconds")

            return {
                "status": "healthy" if not issues else "degraded",
                "issues": issues,
                "slave_status": slave_status
            }
        except Exception as e:
            return {"status": "not_applicable", "message": str(e)}

    def get_summary(self) -> str:
        """Get log analysis summary"""
        analysis = self.analyze()
        summary = f"Log Analysis by {self.name}:\n"

        error_info = analysis["error_count"]
        if error_info.get("count", 0) > 0:
            summary += f"⚠️  {error_info.get('message')}: {error_info['count']} aborted connections\n"
        else:
            summary += "✓ No significant connection errors\n"

        common_errors = analysis["common_errors"]
        if common_errors.get("count", 0) > 0:
            summary += f"📋 Found {common_errors['count']} distinct error types\n"

        warnings = analysis["warning_events"]
        if warnings.get("warning_count", 0) > 0:
            summary += f"⚠️  {warnings['warning_count']} system warnings detected\n"

        return summary
