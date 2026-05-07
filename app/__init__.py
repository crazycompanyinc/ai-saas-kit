"""FastAPI application factory for AI SaaS Kit."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.routes import api_router
from app.core.config import settings
from app.core.database import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables on startup."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        description="Open-source starter kit to launch your AI-powered SaaS in minutes",
        version="0.1.0",
        lifespan=lifespan,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Static files
    static_dir = Path(__file__).parent / "static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    # API routes
    app.include_router(api_router, prefix="/api/v1")

    # Health check
    @app.get("/health", tags=["health"])
    async def health():
        return {"status": "healthy", "version": "0.1.0"}

    # Template-based frontend routes
    templates_dir = Path(__file__).parent / "templates"
    templates = Jinja2Templates(directory=str(templates_dir))

    @app.get("/", include_in_schema=False)
    async def landing(request):
        from fastapi import Request
        return templates.TemplateResponse("landing.html", {"request": request})

    @app.get("/docs-api", include_in_schema=False)
    async def docs_page(request):
        from fastapi import Request
        return templates.TemplateResponse("docs.html", {"request": request})

    return app
