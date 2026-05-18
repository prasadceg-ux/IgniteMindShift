"""Aggregates all v1 API routers."""

from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.districts import router as districts_router
from app.api.v1.schools import router as schools_router

v1_router = APIRouter(prefix="/api/v1")

# Phase 1: Auth & Profile
v1_router.include_router(auth_router, tags=["Auth & Profile"])
v1_router.include_router(districts_router, tags=["Districts"])
v1_router.include_router(schools_router, tags=["Schools"])

# Future phases will add more routers here:
# v1_router.include_router(courses_router, tags=["Courses"])
# v1_router.include_router(feed_router, tags=["Feed"])
# v1_router.include_router(exams_router, tags=["Exams"])
# v1_router.include_router(chat_router, tags=["AI Tutor"])
# v1_router.include_router(gamification_router, tags=["Gamification"])
# v1_router.include_router(admin_router, tags=["Admin"])
