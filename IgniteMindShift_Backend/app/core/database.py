"""
Async SQLAlchemy database engine and session management.

SQLite for local development, swap DATABASE_URL to PostgreSQL for production.
The only SQLite-specific bit is the 'connect_args' for check_same_thread.
Everything else (models, queries, sessions) works identically on both.
"""

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import event

from app.config import settings


# ---------- Engine ----------

connect_args = {}
if settings.is_sqlite:
    # SQLite needs this for async usage
    connect_args["check_same_thread"] = False

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    connect_args=connect_args,
    # For PostgreSQL, you'd tune pool_size, max_overflow, pool_recycle here.
    # SQLite ignores pool settings since it's file-based.
)

# Enable WAL mode and foreign keys for SQLite (performance + integrity)
if settings.is_sqlite:
    @event.listens_for(engine.sync_engine, "connect")
    def _set_sqlite_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


# ---------- Session Factory ----------

async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ---------- Base ----------

class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


# ---------- Dependency ----------

async def get_db() -> AsyncSession:
    """FastAPI dependency — yields an async session, auto-closes."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# ---------- Init ----------

async def init_db():
    """Create all tables. Called once at startup."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """Dispose engine. Called at shutdown."""
    await engine.dispose()
