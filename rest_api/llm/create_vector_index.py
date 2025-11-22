from langchain_google_genai import GoogleGenerativeAIEmbeddings
from functools import lru_cache
from llm.mongo_itaivan import collect_informations, salvar_novos_no_mongo
from config import Settings

settings = Settings()

fields = ["numerobanhos", "numeroquartos", "numerosuites", "numerovagas", "valor", "areainterna"]

GOOGLE_API_KEY = settings.google_api_key

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
    embedding_vector = embeddings_model.embed_query(embedding_text) 
    
    return {
        "embedding_vector": embedding_vector,
        "embeddings_text": embedding_text,
    }


def inserir_propriedades():

    properties_list = collect_informations()
    properties_with_embeddings = []

    for property in properties_list:
        embeddings = generate_embeddings(property)
        properties_with_embeddings.append(dict(property, **embeddings))
        

    salvar_novos_no_mongo(properties_with_embeddings)


if __name__ == "__main__":
    inserir_propriedades()
    print("Propriedades inseridas com sucesso!")

   