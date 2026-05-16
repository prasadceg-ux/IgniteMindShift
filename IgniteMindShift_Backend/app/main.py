"""
Ignite Mindshift API — Application Entry Point.

Run with:  uvicorn app.main:app --reload
Docs at:   http://localhost:8000/docs
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.core.database import close_db, async_session_factory
from app.api.v1.router import v1_router
from app.schemas.common import HealthCheck
from app.utils.seed_districts import seed_districts

# Import unrouted models so they register with Base.metadata (for Alembic autogenerate)
import app.models.user          # noqa: F401
import app.models.course        # noqa: F401
import app.models.progress      # noqa: F401
import app.models.exam          # noqa: F401
import app.models.feed          # noqa: F401
import app.models.chat          # noqa: F401
import app.models.gamification  # noqa: F401
import app.models.synthesia     # noqa: F401
import app.models.notification  # noqa: F401


# ──────────────────────────────────────────────
# Lifespan — startup / shutdown
# ──────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_session_factory() as db:
        await seed_districts(db)
        await db.commit()
    yield
    # Shutdown: clean up connections
    await close_db()
    print("✓ Database connections closed")


# ──────────────────────────────────────────────
# App Factory
# ──────────────────────────────────────────────

app = FastAPI(
    title=settings.APP_NAME,
    description="Crowdsourced mobile learning platform API",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS — allow the React Native / Expo dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ──────────────────────────────────────────────
# Health Check
# ──────────────────────────────────────────────

@app.get("/health", response_model=HealthCheck, tags=["System"])
async def health_check():
    return HealthCheck(app=settings.APP_NAME, environment=settings.APP_ENV)


# ──────────────────────────────────────────────
# Mount Routers
# ──────────────────────────────────────────────

app.include_router(v1_router)
