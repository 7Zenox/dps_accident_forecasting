import secrets

from fastapi import Security, status
from fastapi.security import APIKeyHeader

from utilities.core.config import settings
from utilities.core.exceptions import CustomHTTPException

internal_api_key_header = APIKeyHeader(name="access_key", auto_error=False)


async def verify_access_key(
    access_key: str = Security(internal_api_key_header),
) -> None:
    if not access_key:
        raise CustomHTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, message="Missing Access Key"
        )

    try:
        internal_api_key = access_key.split("token ")[1]
    except Exception:
        raise CustomHTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, message="Invalid Access Key"
        )

    if not secrets.compare_digest(settings.INTERNAL_API_KEY, internal_api_key):
        raise CustomHTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, message="Invalid Access Key"
        )
