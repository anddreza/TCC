from fastapi import FastAPI
from routers.properties import properties_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get("/")
def found_data():     
    return { 
        "example_result": True 
    } 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(properties_router)
