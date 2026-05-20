"""FastAPI application for MySQL RCA"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.router.diagnostic import router as diagnostic_router
from app.core.database import db_manager

app = FastAPI(
    title="MySQL RCA API",
    description="Multi-Agent Root Cause Analysis System for MySQL",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(diagnostic_router)


@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    print("MySQL RCA API starting up...")
    if db_manager.test_connection():
        print("✓ Database connection successful")
    else:
        print("⚠️  Database connection failed")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("MySQL RCA API shutting down...")
    db_manager.close()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "MySQL RCA API",
        "version": "0.1.0",
        "docs": "/docs"
    }


@app.get("/status")
async def status():
    """Get system status"""
    return {
        "status": "running",
        "database": "connected" if db_manager.test_connection() else "disconnected"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
