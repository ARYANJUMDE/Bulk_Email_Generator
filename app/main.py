"""
Main application entry point for the Bulk Certificate Generator Backend.
"""

from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

from app.models import CERTS_DIR
from app.routes import router
from app.storage import jobs
from app.ui import get_dashboard_html

# Ensure output directory exists
CERTS_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="Bulk Certificate Generator",
    description="""
    Backend API that accepts certificate generation requests for a list of recipients 
    and generates professional certificates based on an elegant template.
    
    Features:
    - Bulk certificate generation from a single API request
    - Input validation & email sanitization
    - Generation status tracking by Job UUID
    - Retrieval and download of generated certificates
    - Graceful failure handling (one failure doesn't block others)
    """,
    version="1.0.0",
)

# Register API routes under /api/v1
app.include_router(router)


@app.get(
    "/",
    tags=["system"],
    summary="Root Web Dashboard & API Discovery",
    description="Serves the interactive Web Dashboard to web browsers, or JSON discovery metadata to API clients.",
)
async def root(request: Request):
    """Root route: Interactive UI for browsers, JSON index for API clients."""
    accept = request.headers.get("accept", "")
    if "text/html" in accept:
        return HTMLResponse(content=get_dashboard_html(), status_code=200)

    return {
        "message": "Bulk Certificate Generator API",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "generate": "/api/v1/generate-certificates",
            "status": "/api/v1/status/{job_id}",
            "certificates": "/api/v1/certificates",
            "download": "/api/v1/certificates/{filename}",
            "health": "/api/v1/health",
        },
    }


__all__ = ["app", "jobs"]