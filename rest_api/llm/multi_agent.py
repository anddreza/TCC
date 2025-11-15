# -*- coding: utf-8 -*-

from crewai import LLM, Agent, Task, Crew
from dotenv import load_dotenv
from crewai_tools import SerperDevTool, MCPServerAdapter
from mcp import StdioServerParameters
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
backend_root = os.path.dirname(os.path.abspath(__file__))

server_params = StdioServerParameters(
    command="python3", 
    args=["properties_mcp_server.py"],
    env={"UV_PYTHON": "3.12",
          **os.environ
    }
)


@tool
def mongodb_tool() -> str:
    """Útil para buscar e recuperar informações de documentos no MongoDB."""
    try:
        #query = eval(query_string) 
        #    results = list(Collection.find(query, limit=5))
        return ["test_id_1"]
    except Exception as e:
        return f"Erro ao executar a consulta no MongoDB: {e}"


def llm_property_search(user_preferences: str):
    with MCPServerAdapter(server_params) as tools:
        print(f"Available tools from Stdio MCP server: {[tool.name for tool in tools]}")
        market_researcher = Agent(
            role="Analista de Busca de Imóveis",
            goal="Utilizar a ferramenta find_properties tool para buscar imóveis conforme os critérios do usuário"
            "Você precisa entender as preferências do usuário, ele passará as informações contando um pouco sobre como ele vive, o que ele faz e o que ele está procurando no apartamento ideal, para você entender melhor muitas pessoas vem de outras cidades trabalhar em empresas na cidade, então talvez encontrar um apartamento de 2 quartos com uma 1 vaga de garagem seja o que normalmente o usuário deseja. "
            "Analise também cada detalhe do que ele enviar e não faça perguntas, trabalhe somente com as informações que foram enviadas, se estiver incompleto faça o melhor possível com o que foi enviado." 
            "Baseado na preferência do usuário procure dentro do banco de dados, não invente IDs, pegue o que já existe e envie a melhor opção para o usuário, conforme as necessidades que foram específicas, pode ser que as informações estejam incompletas e meio vagas, porém nem sempre o usuário irá ceder todas as informações necessárias.",
            backstory="Um analista automatizado que entende as preferências do usuário e usa a ferramenta find_properties tool para buscar imóveis compatíveis.",
            tools=tools,
            verbose=True, 
            allow_delegation=False, 
            llm = LLM(model="gemini/gemini-2.0-flash", api_key=GOOGLE_API_KEY)
        )
        task_market_researcher = Task(
            description=(
                f"Preferências do usuário: {user_preferences}"
                "Compile as preferências do usuário em um dicionário Python com as seguintes propriedades:"
                "Ignore quaisquer ambiguidades, invente o que for necessário para preencher o tipo, as comodidades e o preço. Chame a ferramenta search_properties e retorne os resultados."
                ""
            ),  
            expected_output=(
                "Mostre o que a Tool está enviando, não altere as informações com mais caracteres trabalhe somente com o que foi retornado. Tool responderá uma lista de strings com os IDs dos imóveis encontrados."
                "Todas as informações tem que ser dada em português para o usuário final."
                "Retorne os IDs dos imóveis encontrados: Example: ['08d03e0f1f1b13923114cd1a']"
                "Não diga nada além do que ele enviar a você, trabalhe somente com as informações que foi enviado."
                "O resultado JSON parsable string"
            ),   
            agent=market_researcher, 
        )
        crew = Crew(
            tasks=[task_market_researcher],
            agents=[market_researcher],
            verbose=True,
            max_rpm=25  
        )

        result = crew.kickoff()
        print(result) 
        
        return result