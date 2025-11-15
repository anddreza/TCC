from mongo_itaivan import aggregate_mongo
from create_vector_index import procurar_banco_dados, get_embeddings_model


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

def create_vector_for_string(search_term):
#    search_vector = procurar_banco_dados(search_term)

    embeddings_model = get_embeddings_model()
    search_embedding_vector = embeddings_model.embed_query(search_term)

    return search_embedding_vector


# 3. Create the mongodb aggregation
def create_aggregation(search_embedding_vector):
    firstStep = {
        "$vectorSearch" : {
            "index": "vector_index",
            "path": "embedding_vector",
            "queryVector": search_embedding_vector,
            "numCandidates": 10,
            "limit": 3
        }
    }

    secondStep = {
        "$project": {
            "_id": 1, 
            "tipo": 1,
            "titulo": 1,
            "codigo": 1,
            "score": { "$meta": "vectorSearchScore" }
        }
    }

    return [firstStep, secondStep]

# 4. Run the aggregation
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