import ssl
from dotenv import load_dotenv
from fastapi import FastAPI
from pymongo import MongoClient
from llm.mongo_itaivan import COLLECTION_NAME, DB_NAME, MONGO_URI
from routers.properties import properties_router, get_properties_collection
from fastapi.middleware.cors import CORSMiddleware
from config import Settings
from contextlib import asynccontextmanager
from fastapi import FastAPI
from llm.job import fake_insert_mongo, insert_mongo
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
 
load_dotenv()
settings = Settings()
scheduler = BackgroundScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):

    scheduler.add_job(
        func=fake_insert_mongo,
        trigger=IntervalTrigger(minutes=1),
        id='get_properties_job',
        name='Get properties job',
        replace_existing=True
    )
    scheduler.start()

    print("Starting schedulers", flush=True)
#     colection = get_properties_collection()

#     colection.create_index([("codigo", 1)], unique=True)
#     count = colection.count_documents({})
#     print(f"Total documents: {count}", flush=True)
#     insert_mongo()
#     count = colection.count_documents({})
#     print(f"Total documents: {count}", flush=True)

    yield
    print("Shutting down schedulers", flush=True)

app = FastAPI(lifespan=lifespan)
    
@app.get("/")
def found_data():     
    return {"example_result": True}
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.allow_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(properties_router)
