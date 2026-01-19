# Portfolio Analysis API

This directory contains the consolidated FastAPI application for the portfolio analysis system.

## Structure

```
src/api/
├── __init__.py          # Package exports
├── app.py               # Main FastAPI application
├── dependencies.py      # Shared dependencies (DB stores, etc.)
├── routers/
│   ├── __init__.py
│   ├── health.py        # Health check and system info endpoints
│   ├── insights.py      # Insights CRUD, customization, and user roles
│   ├── projects.py      # Project management (thumbnails, etc.)
│   └── consent.py       # Privacy consent management
└── README.md           # This file
```

## Running the API

### Development Server

```bash
# From the project root
cd src
python -m uvicorn api.app:app --reload --host 0.0.0.0 --port 8000
```

Or run directly:

```bash
cd src
python api/app.py
```

### Production Server

```bash
cd src
uvicorn api.app:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

Once the server is running, visit:

- **Interactive API docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative docs (ReDoc)**: http://localhost:8000/redoc
- **OpenAPI schema**: http://localhost:8000/openapi.json

## Available Endpoints

### Health & System
- `GET /` - Root endpoint with API information
- `GET /health` - Health check

### Insights (`/insights`)
- `DELETE /insights/` - Delete all insights
- `DELETE /insights/zips/{zip_hash}` - Delete insights for a zip
- `DELETE /insights/projects/{zip_hash}/{project_name}` - Delete project insights
- `PATCH /insights/portfolio/{project_info_id}` - Update portfolio customization
- `GET /insights/projects/{zip_hash}/{project_name}` - Get project with user role
- `PUT /insights/projects/{zip_hash}/{project_name}/role` - Set user role

### Projects (`/projects`)
- `GET /projects/{project_name}/thumbnail` - Thumbnail upload form
- `POST /projects/{project_name}/thumbnail` - Upload project thumbnail

### Privacy Consent (`/privacy-consent`)
- `POST /privacy-consent/` - Grant privacy consent (LLM, directory, or both)
- `DELETE /privacy-consent/` - Revoke privacy consent
- `GET /privacy-consent/` - Get all consent status
- `GET /privacy-consent/llm` - Get LLM consent status
- `GET /privacy-consent/directory` - Get directory consent status
- `POST /privacy-consent/reset` - Reset all consents to default
- `PATCH /privacy-consent/directory/paths` - Update allowed directory paths

## Environment Variables

- `DATABASE_URL` - Database connection string (defaults to SQLite in data directory)

## CORS Configuration

Currently configured to allow all origins (`*`). Update `app.py` for production:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Restrict origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)
```

## Adding New Endpoints

1. Create a new router in `routers/` (or add to existing)
2. Define your endpoints using `@router.get()`, `@router.post()`, etc.
3. Import and include the router in `app.py`:

```python
from api.routers import your_new_router

app.include_router(your_new_router.router)
```

## Dependencies

Shared dependencies are defined in `dependencies.py`:
- `get_insights_store()` - Get ProjectInsightsStore instance
- `get_role_store()` - Get ProjectRoleStore instance
- `resolve_db_path()` - Resolve database path from environment

Use them in your endpoints:

```python
from api.dependencies import get_insights_store
from insights.storage import ProjectInsightsStore

@router.get("/example")
def example(store: ProjectInsightsStore = Depends(get_insights_store)):
    # Use store here
    pass
```
