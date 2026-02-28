"""
FastAPI application entry point for the PropTech property search backend.
Serves the REST API and integrates with MySQL and Ollama.
"""

import logging
import sys
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.routes import api_router, router as routes_router

logger = logging.getLogger(__name__)

# ANSI color codes for terminal output
_COLORS = {
    logging.DEBUG: "\033[36m",  # cyan
    logging.INFO: "\033[32m",  # green
    logging.WARNING: "\033[33m",  # yellow
    logging.ERROR: "\033[31m",  # red
    logging.CRITICAL: "\033[31;1m",  # bold red
}
_RESET = "\033[0m"


class ColoredLevelFormatter(logging.Formatter):
    """Format log messages with level name colored by severity."""

    def format(self, record: logging.LogRecord) -> str:
        color = _COLORS.get(record.levelno, _RESET)
        record.levelname = f"{color}{record.levelname}{_RESET}"
        return super().format(record)


def _configure_logging() -> None:
    """Configure app loggers to use colored output (WARNING=yellow, ERROR=red, etc.)."""
    app_logger = logging.getLogger("app")
    app_logger.setLevel(logging.DEBUG)
    app_logger.propagate = False  # only our handler, so uvicorn access logs stay as-is
    if not app_logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            ColoredLevelFormatter("%(levelname)s: %(name)s - %(message)s")
        )
        app_logger.addHandler(handler)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan: startup and shutdown hooks."""
    _configure_logging()
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
