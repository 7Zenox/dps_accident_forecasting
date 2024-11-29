from fastapi import APIRouter

from utilities.api.v1.endpoints import (
    accident
)

api_router = APIRouter()
api_router.include_router(accident.router, prefix="/accident")