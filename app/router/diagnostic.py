"""API routes for MySQL RCA diagnostics using deepagents"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from app.agents.main_agent import diagnose_database, create_rca_agent
from app.core.database import db_manager

router = APIRouter(prefix="/api/v1/diagnostic", tags=["diagnostic"])


class DiagnosticRequest(BaseModel):
    """Request model for diagnostic"""
    issue_description: Optional[str] = None
    detailed: bool = False


class AnalysisResult(BaseModel):
    """Analysis result model"""
    status: str
    issue_description: Optional[str]
    findings_summary: Dict[str, str]
    recommendations: List[str]
    analysis: Optional[str] = None


class HealthCheckResponse(BaseModel):
    """Health check response"""
    database_connected: bool
    status: str


class PerformanceMetrics(BaseModel):
    """Performance metrics"""
    slow_queries: int
    active_connections: int
    connection_utilization: float
    buffer_pool_hit_ratio: str


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Check system health"""
    db_connected = db_manager.test_connection()

    return HealthCheckResponse(
        database_connected=db_connected,
        status="healthy" if db_connected else "degraded"
    )


@router.post("/analyze", response_model=AnalysisResult)
async def analyze_issue(request: DiagnosticRequest):
    """Analyze a database issue using deepagents multi-agent system"""
    try:
        result = diagnose_database(request.issue_description or "")

        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result.get("message", "Analysis failed"))

        analysis_text = result.get("analysis", "")

        return AnalysisResult(
            status="complete",
            issue_description=result.get("issue_description"),
            findings_summary={},
            recommendations=[],
            analysis=analysis_text if request.detailed else None
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/report")
async def get_report(issue: Optional[str] = None):
    """Get detailed diagnostic report from deepagents analysis"""
    try:
        result = diagnose_database(issue or "General MySQL database diagnosis")

        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result.get("message"))

        return {
            "report": result.get("analysis", ""),
            "status": result["status"],
            "issue": result.get("issue_description")
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")


@router.get("/metrics", response_model=PerformanceMetrics)
async def get_performance_metrics():
    """Get current performance metrics"""
    try:
        from app.agents.subagents import PerformanceAnalyzer

        perf = PerformanceAnalyzer()
        analysis = perf.analyze()

        slow_queries = analysis.get("slow_queries", {})
        conn_info = analysis.get("connection_info", {})
        cache = analysis.get("cache_efficiency", {})

        return PerformanceMetrics(
            slow_queries=slow_queries.get("count", 0),
            active_connections=conn_info.get("active_connections", 0),
            connection_utilization=conn_info.get("utilization_percent", 0),
            buffer_pool_hit_ratio=cache.get("buffer_pool_hit_ratio", "0%")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Metrics retrieval failed: {str(e)}")


@router.get("/slow-queries")
async def get_slow_queries(limit: int = 10):
    """Get slow queries"""
    try:
        queries = db_manager.get_slow_queries(limit=limit)
        return {"slow_queries": queries}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch slow queries: {str(e)}")


@router.get("/table-stats")
async def get_table_statistics():
    """Get table statistics"""
    try:
        stats = db_manager.get_table_statistics()
        return {"tables": stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch table stats: {str(e)}")


@router.get("/lock-info")
async def get_lock_info():
    """Get lock information"""
    try:
        locks = db_manager.get_lock_info()
        return {"locks": locks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch lock info: {str(e)}")


@router.get("/process-list")
async def get_process_list():
    """Get current process list"""
    try:
        processes = db_manager.get_process_list()
        return {"processes": processes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch process list: {str(e)}")
