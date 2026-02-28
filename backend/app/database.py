"""
Async database connection and session management for MySQL (aiomysql).
Uses environment variables: MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD.
"""

import os
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Build connection URL from environment (aiomysql driver)
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DATABASE = os.environ["MYSQL_DATABASE"]
MYSQL_USER = os.environ["APP_MYSQL_USER"]
MYSQL_PASSWORD = os.environ["APP_MYSQL_PASSWORD"]

DATABASE_URL = (
    f"mysql+aiomysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
    f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)

engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=os.getenv("SQL_ECHO", "0").lower() in ("1", "true"),
)

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency that yields an async DB session; closes it after request."""
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
