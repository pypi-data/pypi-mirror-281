from typing import Callable

from fastapi.exceptions import RequestValidationError
from starlette import status
from fastapi import Request
from starlette.responses import JSONResponse

from known_problems_fastapi_router.types import KnownProblemResponse


def build_validation_error_exception_handler(
    base_uri: str,
) -> Callable[[Request, RequestValidationError], JSONResponse]:
    def exception_handler(request: Request, exc: RequestValidationError):
        detail = ", ".join(
            [f"{error.get('loc')[1]}: {error.get('msg')}" for error in exc.errors()]
        )
        instance = f"{request.method}:/{request.url}"
        response = KnownProblemResponse(
            type=f"problem:{base_uri}/unprocessable-entity",
            title="Schema validation failed",
            status=422,
            detail=detail,
            instance=instance,
        )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=response.model_dump(mode="json"),
        )

    return exception_handler
