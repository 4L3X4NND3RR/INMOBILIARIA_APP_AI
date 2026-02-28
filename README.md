# PropTech Property Search

REST API and Vue.js frontend for searching real estate properties using **natural language**. The backend uses a local LLM (Ollama) to convert your query into SQL, runs it on MySQL, and returns the results.

## Features

- **Natural-language search**: e.g. “casas de 3 habitaciones en menos de 200000” → translated to SQL and executed
- **FastAPI backend**: async, OpenAPI docs at `/docs`
- **Vue 3 + Vite frontend**: simple search UI
- **Docker Compose**: MySQL, backend, and frontend in one stack
- **Ollama integration**: runs on your host; backend connects via `host.docker.internal`

## Architecture

```
User query (natural language)
    → Frontend (Vue) → Backend (FastAPI)
    → Ollama (LLM: NL → SQL)
    → MySQL (propiedades table)
    → JSON response
```

| Component | Tech |
|-----------|------|
| **Backend** | FastAPI, SQLAlchemy, httpx |
| **Database** | MySQL 8 |
| **LLM** | Ollama (e.g. `llama3.2:3b`) |
| **Frontend** | Vue 3, Pinia, Axios, Vite |

## Prerequisites

- **Docker** and **Docker Compose**
- **Ollama** installed and running on your machine (same host as Docker)
  - Install: [ollama.com](https://ollama.com)
  - Run: open the Ollama app or `ollama serve`
  - Pull model: `ollama pull llama3.2:3b` (or the model set in `.env`)

## Quick start

### 1. Clone and configure

```bash
git clone <repo-url>
cd REST_API_INMOBILIARIA
```

Copy environment variables and adjust if needed:

```bash
cp .env.example .env
# Edit .env: MySQL passwords, OLLAMA_URL (see below)
```

If there is no `.env.example`, create a `.env` in the project root with at least:

```env
# MySQL
MYSQL_ROOT_PASSWORD=rootpassword
MYSQL_DATABASE=inmobiliaria
MYSQL_USER=app_user
MYSQL_PASSWORD=app_password
APP_MYSQL_USER=proptech_ro
APP_MYSQL_PASSWORD=your_app_password

# Ollama (backend runs in Docker; use host.docker.internal to reach host)
OLLAMA_URL=http://host.docker.internal:11434
OLLAMA_MODEL=llama3.2:3b
OLLAMA_TIMEOUT=60
```

### 2. Run with Docker Compose

```bash
docker compose up -d
```

This starts:

- **MySQL** on port `3306`
- **Backend** on port `8000`
- **Frontend** on port `5173` (served by nginx in the container)

Wait for MySQL to be healthy (about 30s on first run).

### 3. Run the SQL scripts (very important — first run)

**Before using the app, you must run the SQL scripts in this exact order.** The backend will not work correctly without the schema, seed data, and app user. **You must use the MySQL root user** to run these scripts (they create the database objects and application user).

From the project root, run:

```bash
# 1. Create tables (schema)
docker exec -i inmobiliaria-mysql mysql -u root -p"$MYSQL_ROOT_PASSWORD" inmobiliaria < backend/persistencia/schema.sql

# 2. Load seed data
docker exec -i inmobiliaria-mysql mysql -u root -p"$MYSQL_ROOT_PASSWORD" inmobiliaria < backend/persistencia/seed_data.sql

# 3. Create the application user (used by the backend)
docker exec -i inmobiliaria-mysql mysql -u root -p"$MYSQL_ROOT_PASSWORD" < backend/persistencia/create_app_user.sql
```

Use the same `MYSQL_ROOT_PASSWORD` as in your `.env`. On Windows (PowerShell), you may need to pass the password differently or run the commands from Git Bash.

Then open:

- **App**: http://localhost:5173  
- **API docs**: http://localhost:8000/docs

## Project structure

```
REST_API_INMOBILIARIA/
├── backend/                 # FastAPI app
│   ├── app/
│   │   ├── main.py           # App entry, CORS, routers
│   │   ├── routes.py         # /, /health, /health/db, /api/search
│   │   ├── llm_service.py    # Ollama client (NL → SQL)
│   │   ├── sql_validator.py  # Safe SELECT only
│   │   ├── database.py       # Async MySQL engine/session
│   │   └── models.py         # SQLAlchemy + Pydantic models
│   ├── persistencia/
│   │   ├── schema.sql
│   │   ├── seed_data.sql
│   │   └── create_app_user.sql
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                 # Vue 3 + Vite
│   ├── src/
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml
├── .env                      # Not committed; copy from .env.example
└── README.md
```

## API overview

| Method | Endpoint        | Description                    |
|--------|-----------------|--------------------------------|
| GET    | `/`             | API info and links             |
| GET    | `/health`       | Liveness                       |
| GET    | `/health/db`    | DB connectivity                |
| POST   | `/api/search`   | Natural-language search (body: `{"query": "..."}`) |

### Example: search

```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "casas con 3 habitaciones"}'
```

Response includes `results`, `sql_query`, and `count`.

## Configuration

### Environment variables

- **MySQL**: `MYSQL_*`, `APP_MYSQL_USER`, `APP_MYSQL_PASSWORD` — used by `docker-compose` and the backend.
- **Ollama**:
  - `OLLAMA_URL`: Backend must reach Ollama here. From inside Docker on Mac/Windows use `http://host.docker.internal:11434`.
  - `OLLAMA_MODEL`: e.g. `llama3.2:3b`.
  - `OLLAMA_TIMEOUT`: Request timeout in seconds (default 60).

### Running without Docker

- **Backend**: `cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload --port 8000`  
  Set `MYSQL_HOST=localhost`, `OLLAMA_URL=http://localhost:11434` (and other vars) in the environment or `.env`.
- **Frontend**: `cd frontend && npm install && npm run dev` (and set `VITE_API_URL` to the backend URL).
- **MySQL**: Run MySQL 8 locally and apply `schema.sql`, `seed_data.sql`, and `create_app_user.sql` in that order.

## Troubleshooting

### “Ollama request timed out”

1. **Ollama must be running** on the host (Ollama app or `ollama serve`).
2. **Correct URL from the backend**:  
   - Backend in Docker (Mac/Windows): use `OLLAMA_URL=http://host.docker.internal:11434` in `.env`.  
   - Backend on host: use `OLLAMA_URL=http://localhost:11434`.
3. **Port**: Ollama’s API is on **11434**, not 1143.
4. **Slower model or first run**: increase `OLLAMA_TIMEOUT` (e.g. 120).

### Database connection errors

- Ensure MySQL is healthy: `docker compose ps` and check the `mysql` service.
- Run the SQL scripts in order (step 3 in Quick start): `schema.sql` → `seed_data.sql` → `create_app_user.sql`.

### CORS

The backend allows all origins in development. Restrict `allow_origins` in `main.py` for production.

## License

See repository license file.
