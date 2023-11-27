from fastapi import Response, Depends
from fastapi.security import HTTPBearer
from core.config import get_authentication_url
from database.database import db
import requests
import json
from bson import ObjectId, json_util
from utilities.error_handler import UnicornException
from utilities import bearer

config = get_authentication_url()
url = config['URL']

user_collection = db['users']
SECRET_KEY = "your-secret-key"
token_scheme = bearer.HTTPBearer()


def get_user_by_email(email: str, _id: str = None):
    query_obj = {"email": email}
    if _id is not None:
        query_obj.update({"_id": ObjectId(_id)})
    query = user_collection.find_one(query_obj)
    return json.loads(json_util.dumps(query))


def get_user_by_userName(userName: str, _id: str = None):
    query_obj = {"userName": userName}
    if _id is not None:
        query_obj.update({"_id": ObjectId(_id)})
    query = user_collection.find_one(query_obj)
    return json.loads(json_util.dumps(query))


def get_user_by_email_userName(userName: str, _id: str = None):
    query_obj = {"userName": userName, "email": userName}
    if _id is not None:
        query_obj.update({"_id": ObjectId(_id)})
    query = user_collection.find_one(query_obj)
    return json.loads(json_util.dumps(query))
    
    
def check_auth(response: Response, token: str = Depends(token_scheme)):
    try:
        if token and token.credentials is not None:
            new_url = f"{url}/decode_token"
            res = requests.post(new_url, data=json.dumps(
                {"token": token.credentials, "app_name": "pmi"}))
            if res.status_code == 200:
                return res.json()
            else:
                err = res.json()
                raise Exception(err['detail'])
        else:
            raise Exception('Not authenticated.')

    except Exception as e:
        raise UnicornException(str(e))


def remove_special_fields(data):
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            if isinstance(value, dict) and ('$oid' in value or '$date' in value):
                new_dict[key] = value.get('$oid', value.get('$date'))
            else:
                new_dict[key] = remove_special_fields(value)
        return new_dict
    elif isinstance(data, list):
        return [remove_special_fields(item) for item in data]
    else:
        return data
