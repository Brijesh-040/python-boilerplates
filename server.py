from fastapi import Body, FastAPI, HTTPException, APIRouter
from routes import user
# from pymongo.results import DeleteResult
# from pymongo.collection import Collection
# from bson import json_util, ObjectId
# from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from utilities.error_handler import UnicornException, unicorn_exception_handler
import datetime
import pytz

# from database.database import db
# collection_list = db.list_collection_names()
# userModel: Collection = db['user']

startup_time: datetime = None
app = FastAPI(
    title='wnc-api',
    description='Wellncity api',
)


@app.exception_handler(UnicornException)
async def global_exception_handler(request, exc):
    return unicorn_exception_handler(request, exc)


@app.on_event("startup")
async def startup_event():
    global startup_time
    current_time = datetime.datetime.now(pytz.utc)
    ist = pytz.timezone('Asia/Kolkata')
    startup_time = current_time.astimezone(ist).strftime("%d/%m/%Y, %H:%M:%S")
    print('Server Started: ', str(datetime.datetime.now()))


@app.on_event("shutdown")
async def shutdown_event():
    print('Server Shutdown: ', datetime.datetime.now())


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

api_router = APIRouter()

api_router.include_router(user.router, prefix="/auth", tags=["Authentication"])
# api_router.include_router(patient.router, prefix="/patient", tags=["Patient"])
# api_router.include_router(client.router, prefix="/client", tags=["Client"])

app.include_router(api_router)


@app.get("/")
def read_root():
    return {
        "up": startup_time,
        # "database": db2
        # ,"database2": get_db2_config()
    }
