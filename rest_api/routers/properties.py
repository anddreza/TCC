import ssl
from fastapi import APIRouter
from pymongo import MongoClient
from llm.multi_agent import llm_property_search
import json
from bson import ObjectId

from llm.mongo_itaivan import COLLECTION_NAME, DB_NAME, MONGO_URI 

properties_router = APIRouter()

@properties_router.get("/properties")
def get_properties(user_preferences: str):
    
    result = llm_property_search(
        user_preferences=user_preferences)
    print("LLM Result:", result)

#In the properties endpoint -> Return { "ids": property_ids } if the LLM worked
#in the frontend we want to save the Ids in the state import {useState} from 'react'

    house = {
        "message": "Here is a property that matches your preferences.",
    }

    ids = parse_id(result.raw)

    return {
        "message": result.raw if len(ids) == 0 else "Here are some matching apartments",
        "ids": ids
        
    }

def parse_id(response: str):
    try:
        data = json.loads(response)
        return data
    except json.JSONDecodeError:
        return []
    
print("---------------------------------")
def findbyId(id: str):
    try:
        cliente = MongoClient(MONGO_URI, serverSelectionTimeoutMS=30000,  tls=True, tlsAllowInvalidCertificates=False, tlsCAFile=ssl.get_default_verify_paths().cafile)

        db = cliente[DB_NAME]
        colecao = db[COLLECTION_NAME]
        
        resultado = colecao.find_one({ "_id": ObjectId(id) }) 
        if resultado:
            # Convert ObjectId to string
            resultado["_id"] = str(resultado["_id"])
        print(resultado)
        return resultado
    
    except Exception as e:
        print(f"Erro ao agregar dados no MongoDB: {e}")
print("---------------------------------")


@properties_router.get("/properties/{id}")
def get_properties_id(id: str):
    #query mongodb to return id 
    print("ID recebido no endpoint:", id)
    result = findbyId(id)
    return result