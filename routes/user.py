from fastapi import APIRouter
from fastapi.security import HTTPBearer
from utilities.error_handler import UnicornException
from database.services import user_service
from utilities import bearer
from database.models import user_model

router = APIRouter()
token_scheme = bearer.HTTPBearer()


@router.post("/sign_up")
def signup(payload: user_model.SignUp):
    try:
        user = user_service.signup(payload)
        if user:
            return {
                "statusCode": 200,
                "status": 'success',
                "message": 'Congratulations, your account has been successfully created.',
            }
        else:
            return {
                "statusCode": 400,
                "error": 'bad_request',
                "message": "Oops! something wasn't right"
            }
    except Exception as e:
        raise UnicornException(str(e))


@router.post("/log_in")
def login(payload: user_model.Login):
    try:
        return user_service.signIn(payload)
    except Exception as e:
        raise UnicornException(str(e))


@router.get("/get_user/{userId}")
def getUserDetails(userId: str):
    try:
        return user_service.getUserDetails(userId)
    except Exception as e:
        raise UnicornException(str(e))


@router.get("/get_user")
def getUserDetails():
    try:
        return user_service.getUser()
    except Exception as e:
        raise UnicornException(str(e))
