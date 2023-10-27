from typing import Annotated
from fastapi import Body, FastAPI, HTTPException
from pymongo.results import DeleteResult
from pymongo.collection import Collection
from bson import json_util, ObjectId
from pydantic import BaseModel, Field

import json

from databas import db
collection_list = db.list_collection_names()
userModel: Collection = db['user']

app = FastAPI()


class userSchema(BaseModel):
    firstName: str
    lastName: str


@app.get("/")
async def root():
    some = userModel.find_one()
    print(some)
    return {"message": collection_list[0]+' collection connected successfully'}


@app.post("/user/createUser", tags=['user'])
async def create_user(payload: Annotated[userSchema, Body(embed=False)]):
    userData = userModel.insert_one(dict(payload))
    if userData:
        return ('user create successfully')


@app.get("/user/getUserList", tags=['user'])
async def get_user():
    userData = json.loads(json_util.dumps(userModel.find()))
    # array null check => if not array
    if not userData:
        raise HTTPException(status_code=404, message="user not found")
    else:
        return userData


@app.get("/user/getUser/{userId}", tags=['user'])
async def get_user(userId: str):
    userData = json.loads(json_util.dumps(
        userModel.find_one({"_id": ObjectId(userId)})))
    # object null check => if object is None
    if userData is None:
        raise HTTPException(status_code=404, message="user not found")
    else:
        return userData


@app.put("/user/updateUser/{userId}", tags=['user'])
async def update_user(userId: str, payload: Annotated[userSchema, Body(embed=False)]):
    updatePaylod = {
        "$set": dict(payload)
    }
    # print(updatePaylod)
    userData = json.loads(json_util.dumps(
        userModel.find_one_and_update({"_id": ObjectId(userId)}, updatePaylod, return_document=True)))
    # print(userData)
    return (userData)


@app.delete("/user/deleteUser/{userId}", tags=['user'])
async def delete_user(userId: str):
    userData: DeleteResult = userModel.delete_one({"_id": ObjectId(userId)})
    if userData.deleted_count > 0:
        raise HTTPException(status_code=404, message="user not found")
    else:
        return ({"message": "user deleted successfully"})
