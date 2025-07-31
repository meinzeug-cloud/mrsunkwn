"""
Mrs-Unkwn API - AI-Powered Tutor App for Teenagers
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from contextlib import asynccontextmanager

# Import configuration
from config import settings

# Import Mrs-Unkwn specific routers
from endpoints.ai_tutor import router as ai_tutor_router
from endpoints.anti_cheat import router as anti_cheat_router
from endpoints.parental_controls import router as parental_controls_router
from endpoints.device_monitoring import router as device_monitoring_router
from endpoints.families import router as families_router
from endpoints.learning_sessions import router as learning_sessions_router
from endpoints.analytics import router as analytics_router
from endpoints.gamification import router as gamification_router
from endpoints.assessments import router as assessments_router
from endpoints.content import router as content_router
from endpoints.users import router as users_router

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info("🚀 Starting Mrs-Unkwn API Server")
    logger.info(f"📝 Version: {settings.app_version}")
    logger.info(f"🔧 Debug mode: {settings.debug}")
    yield
    # Shutdown
    logger.info("⏹️ Shutting down Mrs-Unkwn API Server")

# Create FastAPI application
app = FastAPI(
    title="Mrs-Unkwn API",
    description="AI-Powered Tutor App for Teenagers with Socratic Method",
    version=settings.app_version,
    lifespan=lifespan
)

# Add security middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"] if settings.debug else ["localhost", "127.0.0.1"]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"] if settings.debug else [],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

# Include Mrs-Unkwn specific routers
app.include_router(ai_tutor_router, tags=["AI Tutor"])
app.include_router(anti_cheat_router, tags=["Anti-Cheat"])
app.include_router(parental_controls_router, tags=["Parental Controls"])
app.include_router(device_monitoring_router, tags=["Device Monitoring"])
app.include_router(families_router, tags=["Family Management"])
app.include_router(learning_sessions_router, tags=["Learning Sessions"])
app.include_router(analytics_router, tags=["Analytics"])
app.include_router(gamification_router, tags=["Gamification"])
app.include_router(assessments_router, tags=["Assessments"])
app.include_router(content_router, tags=["Content"])
app.include_router(users_router, tags=["Users"])

# Health check endpoints
@app.get("/", response_model=dict)
async def root():
    """Root endpoint with basic app information"""
    return {
        "app": "Mrs-Unkwn",
        "description": "AI-Powered Tutor App for Teenagers",
        "version": settings.app_version,
        "status": "operational",
        "features": [
            "Socratic Method AI Tutoring",
            "Anti-Cheating Detection", 
            "Parental Controls",
            "Device Monitoring",
            "Learning Analytics",
            "Gamification"
        ]
    }

@app.get("/health", response_model=dict)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "version": settings.app_version
    }

@app.get("/api/status", response_model=dict)
async def api_status():
    """API status endpoint with detailed information"""
    return {
        "api_status": "operational",
        "version": settings.app_version,
        "debug": settings.debug,
        "features": {
            "ai_tutoring": True,
            "anti_cheat": settings.ai_detection_enabled,
            "parental_controls": True,
            "device_monitoring": settings.enable_monitoring,
            "analytics": settings.enable_analytics
        },
        "limits": {
            "max_session_duration": settings.max_session_duration_minutes,
            "default_difficulty": settings.default_difficulty_level,
            "max_hints": settings.max_hint_count
        }
    }

# Global exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Global HTTP exception handler"""
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "app": "Mrs-Unkwn"
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler for unexpected errors"""
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "status_code": 500,
            "app": "Mrs-Unkwn"
        }
    )

# Main execution
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=settings.api_host,
        port=settings.api_port,
        workers=settings.api_workers,
        reload=settings.debug,
        log_level="info"
    )