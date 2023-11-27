from fastapi import APIRouter, Depends
from core.config import get_authentication_url
from fastapi.security import HTTPBearer
from utilities.error_handler import UnicornException
from utilities.helper import check_auth, remove_special_fields
from database.services import user_service
from utilities import bearer
from database.models import user_model
import requests
import json

config = get_authentication_url()
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


# @router.get("/get_user")
# def getUser(userId: str):
#         userData = json.loads(json_util.dumps(userModel.find()))
#         # array null check => if not array
#         if not userData:
#             raise HTTPException(status_code=404, message="user not found")
#         else:
#             return userData
