from fastapi import FastAPI, HTTPException
from bson import json_util
import json

from databas import db
collection_list = db.list_collection_names()
userModel = db['user']

app = FastAPI()


@app.get("/")
async def root():
    some = userModel.find_one()
    print(some)
    return {"message": collection_list[0]+' collection connected successfully'}


@app.post("/user/create")
async def create_user(firstName: str | None = None, lastName: str | None = None):
    return userModel.insert_one({firstName: firstName, lastName: lastName})


@app.get("/user/getuserList")
async def get_user():
    userData = json.loads(json_util.dumps(userModel.find()))
    print(userData)
    # array null check => if not array
    # object null check => if object is None
    if not userData: 
        raise HTTPException(status_code=404, detail="user not found")
    else:
        return userData
