"""
Auth API routes — registration, login, token refresh, profile.

POST /auth/register   → Create account, return tokens
POST /auth/login      → Authenticate, return tokens (JSON — mobile app)
POST /auth/token      → Authenticate, return tokens (form — Swagger UI)
POST /auth/refresh    → Exchange refresh token for new pair
GET  /profile/me      → Authenticated user's profile
PUT  /profile/me      → Update profile fields
"""

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    RefreshRequest,
    MessageResponse,
)
from app.schemas.user import UserProfile, UserUpdate
from app.services.auth_service import register_user, login_user, refresh_tokens
from app.models.user import User

router = APIRouter()


# ──────────────────────────────────────────────
# Registration & Login
# ──────────────────────────────────────────────

@router.post("/auth/register", response_model=TokenResponse, status_code=201)
async def register(body: RegisterRequest, db: AsyncSession = Depends(get_db)):
    """Create a new student account and return JWT tokens."""
    tokens = await register_user(
        db=db,
        email=body.email,
        name=body.name,
        password=body.password,
    )
    return tokens


@router.post("/auth/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Authenticate with email + password (JSON body). Used by the mobile app."""
    tokens = await login_user(db=db, email=body.email, password=body.password)
    return tokens


@router.post("/auth/token", response_model=TokenResponse, include_in_schema=False)
async def login_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """
    Form-based login for Swagger UI's Authorize button.
    Uses 'username' field as email (Swagger's OAuth2 convention).
    The mobile app uses /auth/login with JSON instead.
    """
    tokens = await login_user(db=db, email=form_data.username, password=form_data.password)
    return tokens


@router.post("/auth/refresh", response_model=TokenResponse)
async def refresh(body: RefreshRequest, db: AsyncSession = Depends(get_db)):
    """Exchange a refresh token for a new token pair."""
    tokens = await refresh_tokens(db=db, refresh_token=body.refresh_token)
    return tokens


# ──────────────────────────────────────────────
# Profile
# ──────────────────────────────────────────────

@router.get("/profile/me", response_model=UserProfile)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    """Return the authenticated user's full profile."""
    return current_user


@router.put("/profile/me", response_model=UserProfile)
async def update_my_profile(
    body: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update the authenticated user's profile fields."""
    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)
    db.add(current_user)
    await db.flush()
    return current_user