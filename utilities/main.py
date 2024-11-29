from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import ORJSONResponse

from utilities.api.health import router as health_check_api_router
from utilities.api.v1.api import api_router as v1_api_router
from utilities.core.exceptions import CustomHTTPException
from utilities.helpers.response import create_response

async def route_not_found(request: Request, exc: HTTPException):
    return create_response(
        status_code=exc.status_code,
        success=False,
        message=exc.detail,
    )

async def internal_server_error(request: Request, exc: HTTPException):
    return create_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        success=False,
        message="Internal Server Error",
    )

app = FastAPI(
    openapi_url=None,
    default_response_class=ORJSONResponse,
    exception_handlers={
        404: route_not_found,
        500: internal_server_error,
    },
)

@app.exception_handler(CustomHTTPException)
async def custom_http_exception_handler(request: Request, exc: CustomHTTPException):
    return create_response(**exc.__dict__)

app.include_router(health_check_api_router)
app.include_router(
    v1_api_router, prefix="/api/v1"
)