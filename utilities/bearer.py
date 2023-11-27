
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.openapi.models import HTTPBearer as HTTPBearerModel
from utilities.error_handler import UnicornException
from starlette.status import  HTTP_403_FORBIDDEN
from fastapi.security import HTTPBasic
from starlette.requests import Request
from pydantic import BaseModel
from typing import Optional

class HTTPAuthorizationCredentials(BaseModel):
    scheme: str
    credentials: str

class HTTPBearer(HTTPBasic):
    def __init__(
        self,
        *,
        bearerFormat: Optional[str] = None,
        scheme_name: Optional[str] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        self.model = HTTPBearerModel(bearerFormat=bearerFormat, description=description)
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error

    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        authorization = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            if self.auto_error:
                raise UnicornException(
                "Not authenticated",  HTTP_403_FORBIDDEN
                )
            else:
                return None
        if scheme.lower() != "bearer":
            if self.auto_error:
                raise UnicornException(
                    "Invalid authentication credentials",HTTP_403_FORBIDDEN
                )
            else:
                return None
        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)