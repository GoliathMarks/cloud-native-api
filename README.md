# cloud-native-api

A cloud-native REST API built with FastAPI, containerized with Docker, and deployed with a GitHub Actions CI pipeline.

## Features

- FastAPI with automatic OpenAPI docs at `/docs`
- Pydantic v2 data validation
- Multi-stage Docker build with non-root user
- Docker Compose for local development
- GitHub Actions CI: lint (ruff), test (pytest), Docker build
- Health check endpoint at `/health`

## Quick Start

### Run locally (no Docker)

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

Visit http://localhost:8000/docs for the interactive API explorer.

### Run with Docker Compose

```bash
docker compose up --build
```

### Run tests

```bash
pytest tests/ -v
```

### Lint

```bash
ruff check .
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Root / status |
| GET | `/health` | Health check |
| GET | `/items` | List all items |
| GET | `/items/{id}` | Get item by ID |
| POST | `/items` | Create an item |
| DELETE | `/items/{id}` | Delete an item |

## Project Structure

```
cloud-native-api/
├── app/
│   ├── main.py              # FastAPI app & router registration
│   ├── routers/
│   │   ├── health.py        # GET /health
│   │   └── items.py         # CRUD /items
│   └── models/
│       ├── health.py        # HealthResponse schema
│       └── item.py          # Item / ItemCreate schemas
├── tests/
│   ├── test_health.py
│   └── test_items.py
├── .github/workflows/
│   └── ci.yml               # Lint → Test → Docker build
├── Dockerfile               # Multi-stage build
├── docker-compose.yml
├── pyproject.toml           # ruff + pytest config
├── requirements.txt
└── requirements-dev.txt
```

## CI Pipeline

On every push / PR to `main`:

1. **Lint** — `ruff check .`
2. **Test** — `pytest tests/ -v`
3. **Docker build** — builds image tagged with the commit SHA (uses GitHub Actions cache for speed)
