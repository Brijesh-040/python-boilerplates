from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class UnicornException(Exception):
    def __init__(self, name: str, status_code: int = 500):
        self.name = name
        self.status_code = status_code


def unicorn_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"err_message": exc.name, "success": False},
    )
