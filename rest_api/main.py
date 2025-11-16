from fastapi import FastAPI
from routers.properties import properties_router
from fastapi.middleware.cors import CORSMiddleware
from config import Settings

app = FastAPI()
settings = Settings()

@app.get("/")
def found_data():     
    print(settings.allow_origin)
    return {"success": True, "message": "API is running"}
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.allow_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(properties_router)
