from llm.create_vector_index import generate_embeddings
from llm.mongo_itaivan import collect_informations, salvar_novos_no_mongo

def insert_mongo():
    pageNumber = 1
    properties_list = []
    while True:
        new_properties = collect_informations(pageNumber)
        pageNumber += 1
        if not new_properties:
            break
        properties_list += new_properties
        if len(new_properties) < 20:
            break
        if pageNumber >= 20:
            break
    print(len(properties_list), flush=True)

    properties_with_embeddings = []
    for property in properties_list:
        
        embeddings = generate_embeddings(property)
        properties_with_embeddings.append(dict(property, **embeddings))

    salvar_novos_no_mongo(properties_with_embeddings)
    print("Job executed: insert_mongo", flush=True)

def fake_insert_mongo():
    print("Job executed: insert_mongo", flush=True)