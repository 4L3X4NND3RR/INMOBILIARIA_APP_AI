"""API routes: root, health, and search."""

import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/")
async def root() -> dict[str, str]:
    """Root endpoint; useful for health checks and discovery."""
    return {
        "message": "PropTech Property Search API",
        "docs": "/docs",
        "api": "/api",
    }


@router.get("/health")
async def health() -> dict[str, str]:
    """Simple health check for Docker/orchestration (app is up)."""
    return {"status": "ok"}


@router.get("/health/db")
async def health_db(db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    """
    Check that the API can connect to the database.
    Returns 200 if connected, 503 if the connection fails.
    """
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        logger.exception("Database health check failed")
        raise HTTPException(
            status_code=503,
            detail={"status": "error", "database": "disconnected", "message": str(e)},
        )


api_router = APIRouter(tags=["api"])


@api_router.post("/search")
async def search():
    """POST /api/search: natural language search - to be implemented."""
    return {"results": [], "count": 0}
