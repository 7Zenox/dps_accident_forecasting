from fastapi import status
from fastapi.responses import ORJSONResponse


def create_response(
    status_code: int = status.HTTP_200_OK,
    success: bool = True,
    message: str = "",
    data: dict = {},
    errors: list = [],
) -> ORJSONResponse:
    content = {
        "success": success,
        "msg": message,
        "data": data,
    }

    if len(errors) > 0:
        content["errors"] = errors

    return ORJSONResponse(
        status_code=status_code,
        content=content,
    )
