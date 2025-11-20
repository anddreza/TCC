from dotenv import load_dotenv
from fastapi import FastAPI
from routers.properties import properties_router
from fastapi.middleware.cors import CORSMiddleware
from config import Settings

load_dotenv()
app = FastAPI()
settings = Settings()

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
