"""Health check endpoint."""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "mimicus",
        "version": "0.1.0",
    }


@router.get("/ready")
async def readiness_check():
    """Readiness check endpoint."""
    return {
        "ready": True,
        "service": "mimicus",
    }
