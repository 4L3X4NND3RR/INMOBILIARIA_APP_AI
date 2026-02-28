"""
FastAPI application entry point for the PropTech property search backend.
Serves the REST API and integrates with MySQL and Ollama.
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.routes import api_router, router as routes_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan: startup and shutdown hooks."""
    yield
    try:
        await engine.dispose()
    except Exception as e:
        logger.warning("Engine dispose failed during shutdown: %s", e)


app = FastAPI(
    title="PropTech Property Search API",
    description="REST API for searching real estate properties using natural language. "
    "Translates NL queries to SQL via Ollama and returns results from MySQL.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS for frontend (Vue.js on port 8080 in Docker)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production (e.g. ["http://localhost:8080"])
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(routes_router)
app.include_router(api_router, prefix="/api")
