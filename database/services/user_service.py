from passlib.context import CryptContext
from bson.objectid import ObjectId
from database.database import db
from utilities import helper
from bson import json_util
import json

from utilities.error_handler import UnicornException

collection = db['users']
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def signup(user):
    try:
        payload = dict(user)
        email_exist = helper.get_user_by_email(payload['email'])
        userName_check = helper.get_user_by_userName(payload['userName'])
        if email_exist is None and userName_check is None:
            payload['password'] = pwd_context.hash(payload['password'])
            payload.pop('cPassword')
            payload.update(
                {
                    "roles": "user",
                }
            )
            _id = collection.insert_one(payload)
            user = json.loads(json_util.dumps(
                collection.find_one({"_id": ObjectId(_id.inserted_id)})))
            return {
                'user': user
            }
        else:
            if email_exist:
                raise UnicornException("User Email already exist.")
            if userName_check:
                raise Exception('User Name already exist.')
    except Exception as e:
        raise e


def signIn(login_details):
    try:
        payload = dict(login_details)
        user = helper.get_user_by_email_userName(payload['userName'])
        if user:
            if pwd_context.verify(payload['password'], user['password']):
                token_payload = {
                    'email': user['email'], '_id': user['_id']['$oid']}
                token = helper.generate_token(token_payload)
                return {
                    "user": user,
                    "token": token
                }
            else:
                raise Exception('Invalid username or password!.')
        else:
            raise Exception('User not exists in database')
    except Exception as e:
        raise e


def getUserDetails(userId):
    try:
        if userId:
            user = json.loads(json_util.dumps(
                collection.find_one({"_id": ObjectId(userId)})))
            return {
                "userDeatils": user
            }
        else:
            raise Exception('User not exists in database')
    except Exception as e:
        raise e


def getUser():
    try:
        return json.loads(json_util.dumps(collection.find({})))
    except Exception as e:
        raise e
