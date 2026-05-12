"""
Authentication service — handles user registration, login, token refresh.

This is the LOCAL auth implementation (email + password + JWT).
When moving to Cognito, replace the internals of these functions
but keep the same function signatures so the routes don't change.
"""

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.core.exceptions import ConflictException, BadRequestException


async def register_user(
    db: AsyncSession,
    email: str,
    name: str,
    password: str,
) -> dict:
    """
    Create a new user account.
    Returns access + refresh tokens so the user is logged in immediately.
    """
    # Check if email already taken
    existing = await db.execute(select(User).where(User.email == email))
    if existing.scalar_one_or_none():
        raise ConflictException("An account with this email already exists")

    user = User(
        email=email,
        name=name,
        hashed_password=hash_password(password),
        last_active=datetime.now(timezone.utc),
    )
    db.add(user)
    await db.flush()  # Get the generated ID without committing

    return {
        "access_token": create_access_token(subject=user.id),
        "refresh_token": create_refresh_token(subject=user.id),
        "token_type": "bearer",
    }


async def login_user(
    db: AsyncSession,
    email: str,
    password: str,
) -> dict:
    """
    Authenticate with email + password.
    Returns tokens on success, raises on failure.
    """
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.hashed_password):
        raise BadRequestException("Invalid email or password")

    if not user.is_active:
        raise BadRequestException("Account is deactivated")

    # Update last active
    user.last_active = datetime.now(timezone.utc)

    return {
        "access_token": create_access_token(subject=user.id),
        "refresh_token": create_refresh_token(subject=user.id),
        "token_type": "bearer",
    }


async def refresh_tokens(db: AsyncSession, refresh_token: str) -> dict:
    """
    Exchange a valid refresh token for a new access + refresh token pair.
    """
    payload = decode_token(refresh_token)

    if payload.get("type") != "refresh":
        raise BadRequestException("Invalid token type — expected a refresh token")

    user_id = payload.get("sub")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user or not user.is_active:
        raise BadRequestException("User not found or deactivated")

    return {
        "access_token": create_access_token(subject=user.id),
        "refresh_token": create_refresh_token(subject=user.id),
        "token_type": "bearer",
    }
