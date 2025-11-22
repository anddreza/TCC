from llm.create_vector_index import generate_embeddings
from llm.mongo_itaivan import collect_informations, salvar_novos_no_mongo


def insert_mongo():
    # properties_list = collect_informations()
    # properties_with_embeddings = []

    # for property in properties_list:
    #     embeddings = generate_embeddings(property)
    #     properties_with_embeddings.append(dict(property, **embeddings))

    # salvar_novos_no_mongo(properties_with_embeddings)
    print("Job executed: insert_mongo", flush=True)