from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError

from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request as StarletteRequest
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


async def http_exception_handler(
    request: StarletteRequest, exc: StarletteHTTPException
) -> JSONResponse:
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)


async def request_validation_exception_handler(
    request: StarletteRequest, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": jsonable_encoder(exc.errors())},
    )


class AppExceptionCase(Exception):
    def __init__(self, status_code: int, context: dict):
        self.exception_case = self.__class__.__name__
        self.status_code = status_code
        self.context = context

    def __str__(self):
        return (
            f"<AppException {self.exception_case} - "
            + f"status_code={self.status_code} - context={self.context}>"
        )


async def app_exception_handler(request: Request, exc: AppExceptionCase):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "app_exception": exc.exception_case,
            "context": exc.context,
        },
    )


class AppException(object):
    class RunProcess(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Process failed
            """
            status_code = 500
            AppExceptionCase.__init__(self, status_code, context)

    class CreateItem(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Item creation failed
            """
            status_code = 500
            AppExceptionCase.__init__(self, status_code, context)

    class GetItem(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Item not found
            """
            status_code = 404
            AppExceptionCase.__init__(self, status_code, context)

    class ItemRequiresAuth(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Item is not public and requires auth
            """
            status_code = 401
            AppExceptionCase.__init__(self, status_code, context)
            

def get_exceptions_for_frontend():
    return [e for e in dir(AppException) if "__" not in e]
    # ['CreateItem', 'GetItem', 'ItemRequiresAuth']