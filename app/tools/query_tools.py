"""Query Analysis Tools for Database Diagnostics"""
from typing import Dict, List, Any, Optional
from datetime import datetime
from app.core.database import db_manager


class QueryAnalyzer:
    """Query analysis tools for optimization and diagnostics"""

    @staticmethod
    def analyze_query_complexity() -> Dict[str, Any]:
        """
        Analyze query complexity and identify complex patterns

        Returns:
            Dictionary with query complexity analysis
        """
        try:
            queries = db_manager.get_slow_queries(limit=20)

            if not queries:
                return {
                    "status": "OK",
                    "message": "No complex queries detected",
                    "complex_queries": 0,
                    "recommendations": []
                }

            # Analyze complexity indicators
            complexity_scores = []
            for query in queries:
                query_text = query.get("query", "")
                score = 0

                # Score based on keywords indicating complexity
                complexity_keywords = {
                    "JOIN": 5,
                    "UNION": 4,
                    "SUBQUERY": 6,
                    "GROUP BY": 3,
                    "HAVING": 3,
                    "ORDER BY": 2,
                    "DISTINCT": 2,
                    "CASE": 2,
                    "WINDOW": 5,
                    "CTE": 4,
                }

                for keyword, points in complexity_keywords.items():
                    if keyword.upper() in query_text.upper():
                        score += points

                complexity_scores.append({
                    "query": query_text[:80],
                    "complexity_score": score,
                    "execution_time": query.get("execution_time", 0)
                })

            # Sort by complexity
            sorted_queries = sorted(complexity_scores, key=lambda x: x["complexity_score"], reverse=True)
            complex_count = len([q for q in complexity_scores if q["complexity_score"] > 10])

            status = "OK"
            if complex_count > 3:
                status = "WARNING"
            if complex_count > 8:
                status = "CRITICAL"

            complexity_analysis = {
                "status": status,
                "message": f"Found {complex_count} highly complex queries",
                "complex_queries": complex_count,
                "top_complex": sorted_queries[:5],
                "recommendations": []
            }

            if complex_count > 0:
                complexity_analysis["recommendations"].extend([
                    "Break down complex queries into simpler components",
                    "Consider using CTEs (Common Table Expressions) for readability",
                    "Evaluate if subqueries can be replaced with JOINs",
                    "Profile execution plans for complex queries"
                ])

            return complexity_analysis

        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Failed to analyze query complexity: {str(e)}",
                "complex_queries": 0,
                "recommendations": []
            }

    @staticmethod
    def analyze_execution_plans() -> Dict[str, Any]:
        """
        Analyze query execution plans and identify inefficiencies

        Returns:
            Dictionary with execution plan analysis
        """
        try:
            queries = db_manager.get_slow_queries(limit=15)

            if not queries:
                return {
                    "status": "OK",
                    "message": "No execution plan issues detected",
                    "inefficient_plans": 0,
                    "recommendations": []
                }

            # Analyze execution patterns
            inefficient_patterns = []
            for query in queries:
                query_text = query.get("query", "")
                exec_time = float(query.get("execution_time", 0))

                # Identify inefficient patterns
                if "SELECT *" in query_text.upper():
                    inefficient_patterns.append({
                        "issue": "SELECT * (unnecessary columns)",
                        "query": query_text[:80],
                        "severity": "medium"
                    })

                if "LIKE '%'" in query_text.upper():
                    inefficient_patterns.append({
                        "issue": "Leading wildcard LIKE (no index usage)",
                        "query": query_text[:80],
                        "severity": "high"
                    })

                if exec_time > 5.0:
                    inefficient_patterns.append({
                        "issue": f"Slow execution ({exec_time}s)",
                        "query": query_text[:80],
                        "severity": "critical"
                    })

            status = "OK"
            if len(inefficient_patterns) > 5:
                status = "WARNING"
            if len(inefficient_patterns) > 10:
                status = "CRITICAL"

            plan_analysis = {
                "status": status,
                "message": f"Found {len(inefficient_patterns)} execution plan issues",
                "inefficient_plans": len(inefficient_patterns),
                "issues": inefficient_patterns[:8],
                "recommendations": []
            }

            if len(inefficient_patterns) > 0:
                plan_analysis["recommendations"].extend([
                    "Use specific column lists instead of SELECT *",
                    "Avoid leading wildcards in LIKE clauses",
                    "Add indexes for frequently searched columns",
                    "Use EXPLAIN PLAN to analyze query execution",
                    "Consider query restructuring or materialized views"
                ])

            return plan_analysis

        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Failed to analyze execution plans: {str(e)}",
                "inefficient_plans": 0,
                "recommendations": []
            }

    @staticmethod
    def analyze_join_patterns() -> Dict[str, Any]:
        """
        Analyze JOIN patterns and identify optimization opportunities

        Returns:
            Dictionary with JOIN pattern analysis
        """
        try:
            queries = db_manager.get_slow_queries(limit=15)

            if not queries:
                return {
                    "status": "OK",
                    "message": "No problematic JOIN patterns detected",
                    "join_issues": 0,
                    "recommendations": []
                }

            # Analyze JOIN patterns
            join_issues = []
            for query in queries:
                query_text = query.get("query", "").upper()
                exec_time = float(query.get("execution_time", 0))

                # Count JOINs
                join_count = query_text.count(" JOIN ")

                if join_count > 4:
                    join_issues.append({
                        "issue": f"Many JOINs ({join_count})",
                        "query": query.get("query", "")[:80],
                        "count": join_count
                    })

                # Detect Cartesian products
                if "WHERE" not in query_text and join_count > 0:
                    join_issues.append({
                        "issue": "Potential Cartesian product (no WHERE clause)",
                        "query": query.get("query", "")[:80],
                        "count": 1
                    })

                # Identify expensive operations
                if exec_time > 3.0 and join_count > 0:
                    join_issues.append({
                        "issue": f"Expensive JOIN ({exec_time}s, {join_count} joins)",
                        "query": query.get("query", "")[:80],
                        "execution_time": exec_time
                    })

            status = "OK"
            if len(join_issues) > 3:
                status = "WARNING"
            if len(join_issues) > 6:
                status = "CRITICAL"

            join_analysis = {
                "status": status,
                "message": f"Found {len(join_issues)} JOIN-related issues",
                "join_issues": len(join_issues),
                "issues": join_issues[:6],
                "recommendations": []
            }

            if len(join_issues) > 0:
                join_analysis["recommendations"].extend([
                    "Limit number of JOINs per query (target: < 5)",
                    "Ensure all JOINs have proper ON conditions",
                    "Add indexes on JOIN columns",
                    "Consider denormalization for frequently joined tables",
                    "Use EXPLAIN to verify JOIN order optimization"
                ])

            return join_analysis

        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Failed to analyze JOIN patterns: {str(e)}",
                "join_issues": 0,
                "recommendations": []
            }

    @staticmethod
    def analyze_subquery_efficiency() -> Dict[str, Any]:
        """
        Analyze subquery usage and efficiency

        Returns:
            Dictionary with subquery analysis
        """
        try:
            queries = db_manager.get_slow_queries(limit=15)

            if not queries:
                return {
                    "status": "OK",
                    "message": "No problematic subqueries detected",
                    "subquery_issues": 0,
                    "recommendations": []
                }

            # Analyze subquery patterns
            subquery_issues = []
            for query in queries:
                query_text = query.get("query", "")
                exec_time = float(query.get("execution_time", 0))

                # Count subqueries
                subquery_count = query_text.count("(SELECT")

                if subquery_count > 2:
                    subquery_issues.append({
                        "issue": f"Multiple subqueries ({subquery_count})",
                        "query": query_text[:80],
                        "count": subquery_count
                    })

                # Identify correlated subqueries
                if "IN (SELECT" in query_text.upper():
                    subquery_issues.append({
                        "issue": "IN with subquery (potentially slow)",
                        "query": query_text[:80],
                        "type": "IN subquery"
                    })

                # Detect nested subqueries
                if subquery_count > 3:
                    subquery_issues.append({
                        "issue": f"Deeply nested subqueries ({subquery_count} levels)",
                        "query": query_text[:80],
                        "depth": subquery_count
                    })

            status = "OK"
            if len(subquery_issues) > 2:
                status = "WARNING"
            if len(subquery_issues) > 4:
                status = "CRITICAL"

            subquery_analysis = {
                "status": status,
                "message": f"Found {len(subquery_issues)} subquery-related issues",
                "subquery_issues": len(subquery_issues),
                "issues": subquery_issues[:6],
                "recommendations": []
            }

            if len(subquery_issues) > 0:
                subquery_analysis["recommendations"].extend([
                    "Replace IN subqueries with JOINs where possible",
                    "Use EXISTS instead of IN for large result sets",
                    "Consider materializing frequently-used subqueries",
                    "Move subqueries to WITH clauses (CTEs) for readability",
                    "Evaluate if subqueries can be indexed or cached"
                ])

            return subquery_analysis

        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Failed to analyze subqueries: {str(e)}",
                "subquery_issues": 0,
                "recommendations": []
            }

    @staticmethod
    def analyze_index_effectiveness() -> Dict[str, Any]:
        """
        Analyze index effectiveness for query optimization

        Returns:
            Dictionary with index effectiveness analysis
        """
        try:
            index_usage = db_manager.get_index_usage()

            if not index_usage:
                return {
                    "status": "UNKNOWN",
                    "message": "Index usage data not available",
                    "index_issues": 0,
                    "recommendations": []
                }

            # Analyze index patterns
            unused_count = 0
            ineffective_count = 0
            index_issues = []

            for idx in index_usage:
                usage_count = idx.get("usage_count", 0)
                index_name = idx.get("index_name", "unknown")

                # Identify unused indexes
                if usage_count == 0:
                    unused_count += 1
                    index_issues.append({
                        "issue": "Unused index (consumes space, slows writes)",
                        "index": index_name,
                        "usage_count": 0
                    })

                # Identify rarely used indexes
                elif usage_count < 5:
                    ineffective_count += 1
                    index_issues.append({
                        "issue": f"Rarely used index ({usage_count} uses)",
                        "index": index_name,
                        "usage_count": usage_count
                    })

            status = "OK"
            if unused_count > 2 or ineffective_count > 5:
                status = "WARNING"
            if unused_count > 5 or ineffective_count > 10:
                status = "CRITICAL"

            index_analysis = {
                "status": status,
                "message": f"Unused: {unused_count}, Ineffective: {ineffective_count} indexes",
                "index_issues": len(index_issues),
                "unused_indexes": unused_count,
                "ineffective_indexes": ineffective_count,
                "issues": index_issues[:8],
                "recommendations": []
            }

            if unused_count > 0:
                index_analysis["recommendations"].extend([
                    f"Drop {unused_count} unused indexes to improve write performance",
                    "Schedule index cleanup after application changes",
                    "Monitor index usage patterns regularly"
                ])

            if ineffective_count > 0:
                index_analysis["recommendations"].extend([
                    "Review rarely used indexes for relevance",
                    "Consider merging similar indexes",
                    "Evaluate index effectiveness for changed workloads"
                ])

            return index_analysis

        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Failed to analyze index effectiveness: {str(e)}",
                "index_issues": 0,
                "recommendations": []
            }

    @staticmethod
    def analyze_query_statistics() -> Dict[str, Any]:
        """
        Analyze query execution statistics and patterns

        Returns:
            Dictionary with query statistics analysis
        """
        try:
            queries = db_manager.get_slow_queries(limit=30)

            if not queries:
                return {
                    "status": "OK",
                    "message": "Query statistics: normal",
                    "total_queries": 0,
                    "recommendations": []
                }

            # Calculate statistics
            total_count = len(queries)
            execution_times = [float(q.get("execution_time", 0)) for q in queries]
            avg_time = sum(execution_times) / len(execution_times) if execution_times else 0
            max_time = max(execution_times) if execution_times else 0
            min_time = min(execution_times) if execution_times else 0

            # Identify patterns
            very_slow = len([t for t in execution_times if t > 10.0])
            slow = len([t for t in execution_times if 1.0 < t <= 10.0])
            moderate = len([t for t in execution_times if 0.1 < t <= 1.0])

            status = "OK"
            if avg_time > 2.0 or very_slow > 5:
                status = "WARNING"
            if avg_time > 5.0 or very_slow > 10:
                status = "CRITICAL"

            statistics = {
                "status": status,
                "message": f"Query statistics: {total_count} queries analyzed",
                "total_queries": total_count,
                "metrics": {
                    "average_time_sec": round(avg_time, 3),
                    "max_time_sec": round(max_time, 3),
                    "min_time_sec": round(min_time, 3),
                    "very_slow_10s_plus": very_slow,
                    "slow_1s_to_10s": slow,
                    "moderate_100ms_to_1s": moderate
                },
                "recommendations": []
            }

            if avg_time > 1.0:
                statistics["recommendations"].append(
                    f"Average query time is {avg_time:.2f}s - investigate slow queries"
                )

            if very_slow > 0:
                statistics["recommendations"].extend([
                    f"Found {very_slow} extremely slow queries (>10s)",
                    "Prioritize optimization of these queries",
                    "Check for missing indexes or query plan issues"
                ])

            return statistics

        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Failed to analyze query statistics: {str(e)}",
                "total_queries": 0,
                "recommendations": []
            }

    @staticmethod
    def identify_missing_indexes() -> Dict[str, Any]:
        """
        Identify missing indexes based on query patterns

        Returns:
            Dictionary with missing index analysis
        """
        try:
            queries = db_manager.get_slow_queries(limit=20)

            if not queries:
                return {
                    "status": "OK",
                    "message": "No missing indexes detected",
                    "suggestions": 0,
                    "recommendations": []
                }

            # Analyze columns frequently used in WHERE clauses
            column_analysis = {}
            suggestions = []

            for query in queries:
                query_text = query.get("query", "").upper()

                # Extract WHERE clause hints
                if "WHERE" in query_text:
                    # Simple pattern matching for column usage
                    where_pos = query_text.find("WHERE")
                    where_clause = query_text[where_pos:where_pos+200]

                    # Identify common columns
                    if "ID" in where_clause:
                        suggestions.append({
                            "suggestion": "Consider adding index on ID columns",
                            "pattern": "ID in WHERE clause",
                            "frequency": "high"
                        })

                    if "DATE" in where_clause or "TIME" in where_clause:
                        suggestions.append({
                            "suggestion": "Consider adding index on date/time columns",
                            "pattern": "DATE/TIME in WHERE clause",
                            "frequency": "high"
                        })

                    if "STATUS" in where_clause:
                        suggestions.append({
                            "suggestion": "Consider adding index on status columns",
                            "pattern": "STATUS in WHERE clause",
                            "frequency": "medium"
                        })

            # Deduplicate suggestions
            unique_suggestions = []
            seen = set()
            for s in suggestions:
                key = s["suggestion"]
                if key not in seen:
                    unique_suggestions.append(s)
                    seen.add(key)

            status = "OK"
            if len(unique_suggestions) > 3:
                status = "WARNING"
            if len(unique_suggestions) > 6:
                status = "CRITICAL"

            index_analysis = {
                "status": status,
                "message": f"Identified {len(unique_suggestions)} index opportunities",
                "suggestions": len(unique_suggestions),
                "missing_indexes": unique_suggestions[:8],
                "recommendations": []
            }

            if len(unique_suggestions) > 0:
                index_analysis["recommendations"].extend([
                    "Evaluate suggested indexes based on query frequency",
                    "Test index creation impact on write performance",
                    "Monitor query performance improvement after indexing",
                    "Consider composite indexes for multiple column matches"
                ])

            return index_analysis

        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Failed to identify missing indexes: {str(e)}",
                "suggestions": 0,
                "recommendations": []
            }

    @staticmethod
    def generate_query_report() -> Dict[str, Any]:
        """
        Generate comprehensive query analysis report

        Returns:
            Complete query analysis report
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "database_info": db_manager.get_database_info(),
            "analyses": {
                "query_complexity": QueryAnalyzer.analyze_query_complexity(),
                "execution_plans": QueryAnalyzer.analyze_execution_plans(),
                "join_patterns": QueryAnalyzer.analyze_join_patterns(),
                "subquery_efficiency": QueryAnalyzer.analyze_subquery_efficiency(),
                "index_effectiveness": QueryAnalyzer.analyze_index_effectiveness(),
                "query_statistics": QueryAnalyzer.analyze_query_statistics(),
                "missing_indexes": QueryAnalyzer.identify_missing_indexes(),
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
def get_query_complexity_report() -> str:
    """Get query complexity analysis report"""
    result = QueryAnalyzer.analyze_query_complexity()
    return f"Status: {result.get('status')}\n{result.get('message')}\nComplex Queries: {result.get('complex_queries')}\nRecommendations: {', '.join(result.get('recommendations', []))}"


def get_execution_plans_report() -> str:
    """Get execution plan analysis report"""
    result = QueryAnalyzer.analyze_execution_plans()
    return f"Status: {result.get('status')}\nIssues Found: {result.get('inefficient_plans')}\nMessage: {result.get('message')}"


def get_join_patterns_report() -> str:
    """Get JOIN patterns analysis report"""
    result = QueryAnalyzer.analyze_join_patterns()
    return f"Status: {result.get('status')}\nJOIN Issues: {result.get('join_issues')}\nMessage: {result.get('message')}"


def get_subquery_efficiency_report() -> str:
    """Get subquery efficiency analysis report"""
    result = QueryAnalyzer.analyze_subquery_efficiency()
    return f"Status: {result.get('status')}\nSubquery Issues: {result.get('subquery_issues')}\nMessage: {result.get('message')}"


def get_index_effectiveness_report() -> str:
    """Get index effectiveness analysis report"""
    result = QueryAnalyzer.analyze_index_effectiveness()
    return f"Status: {result.get('status')}\nUnused Indexes: {result.get('unused_indexes')}, Ineffective: {result.get('ineffective_indexes')}"


def get_query_statistics_report() -> str:
    """Get query statistics analysis report"""
    result = QueryAnalyzer.analyze_query_statistics()
    metrics = result.get('metrics', {})
    return f"Status: {result.get('status')}\nTotal Queries: {result.get('total_queries')}\nAvg Time: {metrics.get('average_time_sec', 0)}s"


def get_missing_indexes_report() -> str:
    """Get missing indexes analysis report"""
    result = QueryAnalyzer.identify_missing_indexes()
    return f"Status: {result.get('status')}\nIndex Suggestions: {result.get('suggestions')}\nMessage: {result.get('message')}"


def get_comprehensive_query_report() -> str:
    """Get comprehensive query analysis report"""
    report = QueryAnalyzer.generate_query_report()

    summary = f"""
COMPREHENSIVE QUERY ANALYSIS REPORT
====================================
Timestamp: {report['timestamp']}
Database: {report['database_info'].get('type')}
Overall Status: {report['overall_status']}

Critical Issues: {', '.join(report['critical_issues']) if report['critical_issues'] else 'None'}

Top Recommendations:
{chr(10).join([f"• {rec}" for rec in report['recommendations'][:7]])}

Detailed Findings:
- Query Complexity: {report['analyses']['query_complexity'].get('status')}
- Execution Plans: {report['analyses']['execution_plans'].get('status')}
- JOIN Patterns: {report['analyses']['join_patterns'].get('status')}
- Subquery Efficiency: {report['analyses']['subquery_efficiency'].get('status')}
- Index Effectiveness: {report['analyses']['index_effectiveness'].get('status')}
- Query Statistics: {report['analyses']['query_statistics'].get('status')}
- Missing Indexes: {report['analyses']['missing_indexes'].get('status')}
"""

    return summary.strip()
