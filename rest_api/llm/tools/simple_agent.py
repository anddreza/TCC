# -*- coding: utf-8 -*-

from crewai import Agent, Task, Crew, LLM
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from crewai_tools import SerperDevTool
from litellm import completion

from pymongo import MongoClient
from llm.tools.query_database import QueryTool


import os
load_dotenv()
query_tool_connection = QueryTool()

os.environ['GEMINI_API_KEY'] = "AIzaSyDZn3o99Y6tEFQ3xfo3Bck69WyTs9BG5zc"
#os.environ['GROQ_API_KEY'] = "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"
#os.environ["SERPER_API_KEY"]= "5eabfc13ab8e09f58bbc2c9ffd7cc0a8434745d9"

corretor_imobiliario = Agent(
    role="secretária de corretor imobiliário",
    goal="você precisa criar uma lista com os id de apartamentos da cidade de jaraguá do sul",
    backstory="você tem habilidade de criar lista com os apartamentos na cidade de jaraguá do sul",
    verbose=True,
    allow_delegation=False, 
    llm="gemini/gemini-2.0-flash",  
)

task_corretor_imobiliario = Task(
    description=(
        "Analise o mercado com o apartamento ideal para o usuário"
        "Estime quantos apartamentos estiver disponível para alugar"
        "Forneça as informações necessárias para o corretor imobiliário experiente."
    ),  
    expected_output=(
        "A saída deve conter os apartamentos com a separação de uma vírgula (exemplo: '123,456,789'), porém se não encontrar apartamentos envie a mensagem Nenhuma propriedade foi encontrada"
        "E uma lista com todos os apartamentos em português"
    ),  
    tools=[query_tool_connection],  
    agent=corretor_imobiliario, 
    output_file='apartamentos.md' 
)

crew = Crew(
    agents=[corretor_imobiliario],
    tasks=[task_corretor_imobiliario], 
    verbose=True,  
    max_rpm=25  # Limita o número de requisições por minuto
)

# Execução do Crew com uma ideia de negócio específica: "oversized tshirts in Mumbai India"
result = crew.kickoff(
    inputs={"ideia": "apartamentos em Jaragua do Sul"}  # Ideia fornecida como entrada para as tarefas
)
print(result)  # Exibe o resultado final das tarefas
