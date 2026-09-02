# Python / FastAPI API Stack — 2026-08 (research backing `fastapi.md`)

Condensed from 3-subagent research fan-out (deleg_07290c6d, 2026-08-05). Live PyPI versions as of Aug 2025/2026.

## Core Toolchain

| Category | Tool | Version |
|---|---|---|
| Framework | FastAPI | 0.141.1 (Python ≥3.10; 3.12+ recommended) |
| ASGI toolkit | Starlette | 1.4.0 |
| Validation | Pydantic | 2.13.4 (Rust core, 10-50x faster than v1) |
| Settings | pydantic-settings | 2.14.2 |
| ORM (primary) | SQLAlchemy | 2.0.51 (async via asyncpg) |
| ORM (simplified) | SQLModel | 0.0.39 (by FastAPI author; Pydantic+SQLAlchemy in one class) |
| ORM (light/async) | Tortoise ORM | 1.1.7 |
| Migrations | Alembic | 1.19.0 |
| Package manager | **uv** | 0.12.1 — new standard; replaces pip+pip-tools+virtualenv; `uv init/add/sync/run` |
| Lint/format | ruff | replaces flake8+isort+black |
| Type check | mypy / pyright | — |
| HTTP client | httpx | async, also used for tests |

## Standard Project Structure (feature-based / Clean Architecture)

```
app/
├── main.py               # app factory, lifespan, middleware (~50 lines, thin)
├── core/                 # config.py (BaseSettings), security.py, database.py, events.py
├── api/
│   ├── dependencies.py   # shared Depends (get_db, get_current_user)
│   └── v1/               # router.py aggregator + endpoints/ per resource
├── features/<name>/      # router.py, models.py (SQLAlchemy), schemas.py (Pydantic),
│                         # service.py (business logic), repository.py (data access), dependencies.py
└── shared/               # cross-cutting utilities
migrations/               # Alembic
tests/                    # conftest.py + features/
```

Layers: Router (interface) → Service (use cases) → Repository (data access) → Models (persistence).

## Key Patterns

- **DI**: `Depends(get_db)`; yield dependencies for resource lifecycle; `Annotated` shorthand (`DB = Annotated[AsyncSession, Depends(get_db)]`); `app.dependency_overrides[...]` for tests; class-based deps with `__call__`.
- **Pydantic v2**: `model_config = ConfigDict(...)`, `model_validate()`/`model_dump()`, `field_validator`/`model_validator`, `Annotated[str, Field(min_length=1)]`, discriminated unions, `@computed_field`, `ConfigDict(strict=True)`.
- **Config**: `BaseSettings` priority = constructor args > env vars > `.env` > defaults. `env_nested_delimiter="__"`. Inject via `Depends(get_settings)`.
- **Lifespan**: `@asynccontextmanager async def lifespan(app)` — replaces deprecated `@app.on_event`.
- **Auth**: OAuth2PasswordBearer + python-jose (RS256 in prod, HS256 dev), passlib[bcrypt], short access (15-30 min) + rotating refresh tokens; **fastapi-users** 15.0.5 for full user management.
- **Rate limiting**: slowapi 0.1.10 (`@limiter.limit("5/minute")` on login etc.).
- **Caching**: fastapi-cache2 0.2.2 (Redis backend, `@cache(expire=60)`); redis-py 8.1.0 (aioredis merged in).
- **Background tasks**: FastAPI BackgroundTasks (fire-and-forget) → ARQ 0.28.0 (async-first, Redis) → Celery 5.6.3 (complex workflows) / Dramatiq 2.2.0. Tasks must be idempotent; DLQ for failures.
- **Versioning**: URL path `/api/v1` per-version routers (recommended); header versioning alternative; `Sunset` header on deprecation.
- **Resilience**: tenacity 9.1.4 (`@retry(stop=stop_after_attempt(3), wait=wait_exponential(...))`), circuitbreaker 2.1.3, httpx timeouts everywhere (connect=5s, read=30s).

## Testing

pytest + pytest-asyncio; `httpx.AsyncClient(app=app, base_url="http://test")` (no server needed); dependency_overrides to swap DB/auth; Testcontainers 4.15.0 (`PostgresContainer("postgres:16")`) for real-DB integration; factory_boy 3.3.3 for fixtures; 80%+ coverage on business logic.

## Observability

- **structlog** 26.1.0 — JSON structured logging; redact PII via custom processor.
- **OpenTelemetry** — `opentelemetry-instrumentation-fastapi` (0.65b0) for traces → Jaeger/Zipkin/OTLP.
- **prometheus-fastapi-instrumentator** 8.1.0 — `/metrics` endpoint.
- **Health checks**: `/health` (liveness) + `/ready` (readiness, checks DB `SELECT 1`).

## Deployment

- ASGI servers: uvicorn (standard) or granian (Rust-based, faster). Production: `gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker`.
- Docker multi-stage with uv: builder `COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv` + `uv sync --frozen --no-dev`; runtime `python:3.12-slim`, `USER nobody`, HEALTHCHECK on `/health`.
- Dev: `fastapi dev` / `fastapi run` (official CLI).

## AI/LLM Integration

- `openai` AsyncOpenAI client; streaming via `StreamingResponse` with `media_type="text/event-stream"` (SSE).
- LangChain / LlamaIndex for chains, agents, RAG; vector DBs: chromadb, qdrant-client, pgvector (SQLAlchemy extension).
- Ollama for local inference (no API keys). Timeout (30s+) and retry on LLM calls; circuit breaker for provider outages; token-budget logging.

## Data Privacy

- structlog redaction processor for PII keys; SQLAlchemy `TypeDecorator` subclass for encrypted columns; audit logging via event listeners; retention/erasure as scheduled jobs (ARQ/Celery); export endpoint returning all user data.

## Sources

FastAPI docs (fastapi.tiangolo.com), Pydantic v2 docs, SQLAlchemy 2.0 docs, PyPI JSON API (live versions).
