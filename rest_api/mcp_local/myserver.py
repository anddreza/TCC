from mcp.server import Server    
from typing import List
from fastapi import APIRouter, Query
from rest_api.llm.vector_search import run_aggregation, search_term_1

server = Server(name="real_state_agent_tools")

properties_router = APIRouter()

@server.tool()
def get_properties():
    properties =  run_aggregation(search_term_1)
    for property in properties:
        if '_id' in property:
            property['_id'] = str(property['_id'])
    print("Properties found:", properties)
    
    return {
        "data": properties
    }


if __name__ == "__main__":
     server.run()
