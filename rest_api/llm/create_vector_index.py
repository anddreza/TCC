from langchain_google_genai import GoogleGenerativeAIEmbeddings
from llm.mongo_itaivan import collect_informations, salvar_novos_no_mongo
from config import Settings

settings = Settings()

fields = ["numerobanhos", "numeroquartos", "numerosuites", "numerovagas", "valor", "areainterna"]

GOOGLE_API_KEY = settings.google_api_key

# config to embeddings model
def get_embeddings_model() -> GoogleGenerativeAIEmbeddings:
    """Get cached embeddings model instance."""
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=GOOGLE_API_KEY,
    )

# create a string to look for in the database
def look_database(real_property):
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
    embedding_text = look_database(rl_property)
    embeddings_model = get_embeddings_model()
    embedding_vector = embeddings_model.embed_query(embedding_text) 
    
    return {
        "embedding_vector": embedding_vector,
        "embeddings_text": embedding_text,
    }


   