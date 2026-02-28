"""
Database and API models for the PropTech property search application.
- SQLAlchemy models: map to MySQL tables.
- Pydantic schemas: request/response validation and serialization for the REST API.
"""

from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import Date, Decimal as SQLDecimal, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# --- SQLAlchemy Base & ORM Model ---


class Base(DeclarativeBase):
    """Base class for SQLAlchemy declarative models."""

    pass


class Propiedad(Base):
    """
    ORM model for the 'propiedades' table.
    Represents a real estate property (casa, departamento, terreno, etc.).
    """

    __tablename__ = "propiedades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=True)
    tipo: Mapped[str] = mapped_column(
        String(64), nullable=False
    )  # casa, departamento, terreno, etc.
    precio: Mapped[Decimal] = mapped_column(SQLDecimal(14, 2), nullable=False)
    habitaciones: Mapped[int] = mapped_column(Integer, nullable=True)
    banos: Mapped[int] = mapped_column(Integer, nullable=True)
    area_m2: Mapped[Optional[Decimal]] = mapped_column(SQLDecimal(10, 2), nullable=True)
    ubicacion: Mapped[str] = mapped_column(String(255), nullable=True)
    fecha_publicacion: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    def __repr__(self) -> str:
        return f"<Propiedad(id={self.id}, titulo={self.titulo!r}, tipo={self.tipo})>"


# --- Pydantic Schemas (API) ---


class PropiedadBase(BaseModel):
    """Base schema with shared fields for Propiedad."""

    titulo: str = Field(..., min_length=1, max_length=255)
    descripcion: Optional[str] = None
    tipo: str = Field(..., min_length=1, max_length=64)
    precio: Decimal = Field(..., ge=0)
    habitaciones: Optional[int] = Field(None, ge=0)
    banos: Optional[int] = Field(None, ge=0)
    area_m2: Optional[Decimal] = Field(None, ge=0)
    ubicacion: Optional[str] = Field(None, max_length=255)
    fecha_publicacion: Optional[date] = None


class PropiedadCreate(PropiedadBase):
    """Schema for creating a new property (e.g. admin endpoints)."""

    pass


class PropiedadResponse(PropiedadBase):
    """Schema for API responses (read); includes id."""

    id: int

    model_config = {"from_attributes": True}


class SearchRequest(BaseModel):
    """Request body for POST /api/search (natural language query)."""

    query: str = Field(..., min_length=1, description="Natural language search query")


class SearchResponse(BaseModel):
    """Response for POST /api/search: list of properties and optional generated SQL."""

    results: list[PropiedadResponse] = Field(default_factory=list)
    sql_query: Optional[str] = Field(
        None, description="Generated SQL (for educational display)"
    )
    count: int = Field(0, description="Number of results returned")
