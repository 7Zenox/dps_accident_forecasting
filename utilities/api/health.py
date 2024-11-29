from fastapi import APIRouter
from utilities.helpers.response import create_response

router = APIRouter()

@router.get("/")
async def check_app_health():
    return("Application is up and running")