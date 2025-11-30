from dotenv import load_dotenv
from fastapi import FastAPI
from database_connection import create_vector_search_index
from routers.properties import properties_router, get_properties_collection
from fastapi.middleware.cors import CORSMiddleware
from config import Settings
from contextlib import asynccontextmanager
from fastapi import FastAPI
from llm.job import insert_mongo
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
 
load_dotenv()
settings = Settings()
scheduler = BackgroundScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    #Create vector search index if it doesn't exist
    #Start the job to insert new properties
    create_vector_search_index()
    properties_collection = get_properties_collection()
    properties_collection.create_index("codigo", unique=True)
    
    scheduler.add_job(
        func=insert_mongo,
        trigger=IntervalTrigger(hours=24),
        id='get_properties_job',
        name='Get properties job',
        replace_existing=True
    )
    scheduler.start()

    print("Starting schedulers", flush=True)
    yield
    print("Shutting down schedulers", flush=True)
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan) # start fastapi 
    
@app.get("/")
def found_data():     
    return {"example_result": True}
     
app.add_middleware(
    CORSMiddleware, # you allow to call API from other origins
    allow_origins=[settings.allow_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(properties_router)
