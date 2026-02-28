"""API routes: root, health, and search."""

import logging

import httpx
from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.llm_service import generate_sql
from app.models import PropiedadResponse, SearchRequest, SearchResponse
from app.sql_validator import get_single_statement, is_safe_sql

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


@api_router.post("/search", response_model=SearchResponse)
async def search(
    body: SearchRequest,
    db: AsyncSession = Depends(get_db),
) -> SearchResponse:
    """
    Search properties by natural language.
    Converts the query to SQL via Ollama, validates it, runs it on MySQL, and returns results.
    """
    query = body.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="query must not be empty")

    # 1. Generate SQL via Ollama
    try:
        raw_sql = await generate_sql(query)
    except httpx.TimeoutException as e:
        logger.warning("Ollama request timed out: %s", e)
        raise HTTPException(
            status_code=504,
            detail="LLM request timed out; try again or check Ollama is running.",
        ) from e
    except httpx.RequestError as e:
        logger.exception("Ollama request failed: %s", e)
        raise HTTPException(
            status_code=503,
            detail="LLM service unavailable; ensure Ollama is running and OLLAMA_URL is correct.",
        ) from e

    if not raw_sql:
        raise HTTPException(
            status_code=422,
            detail="Could not generate SQL from the query; try rephrasing.",
        )

    # 2. Take first statement and validate (only allow safe SELECT)
    sql = get_single_statement(raw_sql)
    logger.info("Generated SQL: %s", sql)
    if not is_safe_sql(sql):
        logger.warning("Rejected unsafe SQL: %s", sql[:200])
        raise HTTPException(
            status_code=400,
            detail="Generated query was not allowed (only SELECT on propiedades is permitted).",
        )

    # 3. Execute on MySQL
    try:
        result = await db.execute(text(sql))
        rows = result.mappings().all()
    except Exception as e:
        logger.exception("SQL execution failed: %s", e)
        raise HTTPException(
            status_code=422,
            detail=f"Query execution failed: {str(e)}",
        ) from e

    # 4. Map rows to API response (handle column names and types)
    results = []
    for row in rows:
        r = dict(row)
        # Ensure date/decimal serialization for JSON
        if "fecha_publicacion" in r and r["fecha_publicacion"] is not None:
            r["fecha_publicacion"] = str(r["fecha_publicacion"])
        if "precio" in r and r["precio"] is not None:
            r["precio"] = float(r["precio"])
        if "area_m2" in r and r["area_m2"] is not None:
            r["area_m2"] = float(r["area_m2"])
        try:
            results.append(PropiedadResponse.model_validate(r))
        except ValidationError as e:
            logger.warning("Row missing required fields for PropiedadResponse: %s", e)
            raise HTTPException(
                status_code=422,
                detail="Generated SQL did not return the expected columns (id, titulo, tipo, precio, etc.).",
            ) from e

    return SearchResponse(
        results=results,
        sql_query=sql,
        count=len(results),
    )
