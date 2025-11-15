# -*- coding: utf-8 -*-

from typing import Collection
from crewai import LLM, Agent, Task, Crew
from dotenv import load_dotenv
from crewai_tools import SerperDevTool
from crewai.tools import tool

from litellm import completion
from pymongo import MongoClient
from llm.tools.query_database import QueryTool

import os

load_dotenv()

query_tool_connection = QueryTool()

os.environ['GROQ_API_KEY'] = "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"
os.environ["SERPER_API_KEY"]= "5eabfc13ab8e09f58bbc2c9ffd7cc0a8434745d9"

GOOGLE_API_KEY = "AIzaSyBHm5HiI_zOWkmFFkCpM8DceLoeU4zAQdo"

@tool
def mongodb_tool() -> str:
    """Útil para buscar e recuperar informações de documentos no MongoDB."""

    try:
        return ["test_id_1"]
    except Exception as e:
        return f"Erro ao executar a consulta no MongoDB: {e}"


simple_agent = Agent(
    role="Analista de Busca de Imóveis",
    goal="Extrair requisitos de imóveis das preferências do usuário e encontrar imóveis correspondentes",
    backstory="Especialista em entender as necessidades do usuário e traduzi-las em critérios de busca de imóveis",
    allow_delegation=False, 
    verbose=True, 
    llm = LLM(model="gemini/gemini-2.0-flash", api_key=GOOGLE_API_KEY)
)


user_preferences="Eu ando de bicicleta com muita frequência, quero ficar perto da minha escola e tenho muitas plantas. Sou estudante e não tenho muito dinheiro"

simple_task = Task(
        description=f"""
        Analyze these user preferences: {user_preferences}
        
        Extract:
        - type (studio, 1br, 2br, etc)
        - price (monthly budget)
        - amenities (list of features they need)
        
        Then use mongodb_tool tool to find matching properties.
        Return ONLY the list of property IDs.
        """,
        expected_output="List of property IDs",
        agent=simple_agent
    )