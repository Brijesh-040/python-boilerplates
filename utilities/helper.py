from fastapi import HTTPException, Response, Depends, status
from fastapi.security import HTTPBearer
import jwt
from database.database import db
import requests
import json
from bson import ObjectId, json_util
from utilities.error_handler import UnicornException
from utilities import bearer
from datetime import datetime, timedelta

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
    query_obj = {
        "$or": [
            {"userName": userName},
            {"email": userName}
        ]
    }
    if _id is not None:
        query_obj.update({"_id": ObjectId(_id)})
    query = user_collection.find_one(query_obj)
    return json.loads(json_util.dumps(query))


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


def generate_token(user: dict):
    expires = datetime.utcnow() + timedelta(hours=24) 
    data = {
        "_id": user['_id']['$oid'],
        "firstName": user['firstName'],
        "lastName": user['lastName'],
        "email": user['email'],
        "roles": user['roles'],
        "exp": expires
    }
    user = dict(data)
    token = jwt.encode(user, SECRET_KEY, algorithm="HS256")
    return token


def check_auth(token: str = Depends(token_scheme)):
    try:
        if token and token.credentials is not None:
            decoded_token = jwt.decode(token.credentials, SECRET_KEY, algorithms=['HS256'])
            return decoded_token
        
        else:
            raise Exception('Not authenticated.')
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except Exception as e:
        raise UnicornException(str(e))
    
    
def create_update_payload(data): 
    if isinstance(data, dict):
        new_data = {key: value for key, value in data.items() if value is not None}
        return { 
            "$set": new_data
        }
    else:
        return data