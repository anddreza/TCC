from langchain_google_genai import GoogleGenerativeAIEmbeddings
from functools import lru_cache
from mongo_itaivan import coletar_dados, salvar_novos_no_mongo

# 1. Identify which fields are important for the search

# numerobanhos - quantos banheiros 
# numeroquartos - quarto sem suite 
# numerosuites  - quarto com suite 
# numerovagas  - garagem 
# valor  
# areainterna

# 2. Create a string with all the information from those fields

fields = ["numerobanhos", "numeroquartos", "numerosuites", "numerovagas", "valor", "areainterna"]

# 3. Generate the vector using google AI model

GOOGLE_API_KEY = "AIzaSyBHm5HiI_zOWkmFFkCpM8DceLoeU4zAQdo"

def get_embeddings_model() -> GoogleGenerativeAIEmbeddings:
    """Get cached embeddings model instance."""
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=GOOGLE_API_KEY,
    )

def procurar_banco_dados(real_property):
    return f""" 
    Tipo: {real_property["tipo"]}. 
    chuveiro: {(real_property["numerobanhos"])} . 
    NumeroDeQuartos: {real_property["numeroquartos"]} .
    NumeroDeSuite: {real_property["numerosuites"]} . 
    Garagem: {real_property["numerovagas"]} .
    Valor: {real_property["valor"]}
    AreaInterna: {real_property["areainterna"]} .
"""


def generate_embeddings(rl_property):
    embedding_text = procurar_banco_dados(rl_property)

    embeddings_model = get_embeddings_model()
    # call server than google gives to us, numero 3 e 4 
    embedding_vector = embeddings_model.embed_query(embedding_text) 
    
    return {
        "embedding_vector": embedding_vector,
        "embeddings_text": embedding_text,
    }


def inserir_propriedades():

    properties_list = coletar_dados(); 
    properties_with_embeddings = []

    for property in properties_list:
        embeddings = generate_embeddings(property)
        properties_with_embeddings.append(dict(property, **embeddings))
        

    salvar_novos_no_mongo(properties_with_embeddings)


if __name__ == "__main__":
    inserir_propriedades()
    print("Propriedades inseridas com sucesso!")

   