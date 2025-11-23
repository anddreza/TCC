from llm.create_vector_index import get_embeddings_model, procurar_banco_dados
from llm.mongo_itaivan import aggregate_mongo
from llm.mongo_itaivan import aggregate_mongo

#from llm.create_vector_index import procurar_banco_dados, get_embeddings_model
#from rest_api.llm.create_vector_index import procurar_banco_dados, get_embeddings_model


# 1. Create our search term
search_term_1 = {
    "tipo": "Apartamento",
    "numerobanhos": 2,
    "numeroquartos": 3,
    "numerosuites": 1,
    "numerovagas": 2,
    "valor": 2500,
    "areainterna": 120
}

search_term_2 = {
    "tipo": "Apartamento",
    "numerobanhos": 2,
    "numeroquartos": 3,
    "numerosuites": 1,
    "numerovagas": 2,
    "valor": 2500,
    "areainterna": 120
}

# 2. Generate a vector for the search property
def create_vector(search_term):
    search_vector = procurar_banco_dados(search_term)

    embeddings_model = get_embeddings_model()
    search_embedding_vector = embeddings_model.embed_query(search_vector)

    return search_embedding_vector


# 3. Create the mongodb aggregation

    # - vector search
def create_aggregation(search_embedding_vector):
    firstStep = {
        "$vectorSearch" : {
            "index": "property_vector_index",
            "path": "embedding_vector",
            "queryVector": search_embedding_vector,
            "numCandidates": 10,
            "limit": 3
        }

    }

    secondStep = {
        "$project": {
            "tipo": 1,
            "titulo": 1,
            "score": { "$meta": "vectorSearchScore" }
        }
    }

    return [firstStep, secondStep]
    # - project

# Run the aggregation
def run_aggregation(search_term):
    vector = create_vector(search_term)
    aggregation =  create_aggregation(vector)
    result = aggregate_mongo(aggregation)

    all_results = result.to_list(length=1)

    return all_results
    

if __name__ == "__main__":
    results = run_aggregation(search_term_1)
    print(results)
    print("Busca finalizada com sucesso!")