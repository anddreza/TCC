from rest_api.properties_mcp_server import find_properties
from rest_api.llm.vector_search import search_term_1

if __name__ == "__main__":
    print("LOOK: " + find_properties(search_term_1) )