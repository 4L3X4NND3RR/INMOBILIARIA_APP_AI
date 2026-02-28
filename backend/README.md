# Backend - API Búsqueda de Propiedades

API REST (FastAPI) para búsqueda de propiedades en lenguaje natural con integración Ollama.

## Estructura

- `app/` - Código de la aplicación
  - `main.py` - Entrada FastAPI
  - `models.py` - Modelos
  - `routes.py` - Rutas API (POST /api/search)
  - `llm_service.py` - Servicio Ollama (NL → SQL)
- `persistencia/` - Scripts de base de datos
  - `schema.sql` - Creación de tablas
  - `seed_data.sql` - Datos de ejemplo

## Requisitos

- Python 3.12+
- MySQL 8
- Ollama (host, fuera de Docker)

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
uvicorn app.main:app --reload --port 8000
```
