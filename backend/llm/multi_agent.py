# -*- coding: utf-8 -*-

from crewai import Agent, Task, Crew
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from crewai_tools import SerperDevTool
from litellm import completion

from pymongo import MongoClient
from tools.query_database import QueryTool


import os

load_dotenv()

query_tool_connection = QueryTool()

os.environ['GROQ_API_KEY'] = "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"
os.environ["SERPER_API_KEY"]= "5eabfc13ab8e09f58bbc2c9ffd7cc0a8434745d9"


def query_mongodb(query_string: str) -> str:
    """
    Executa uma consulta no MongoDB e retorna o resultado.
    A string de consulta deve ser um JSON válido para a query do find.
    Exemplo: {"nome": "produto_exemplo"}
    """
    try:
        # Tenta converter a string de consulta para um dicionário Python
        query = eval(query_string) 
        
        # Executa a busca no MongoDB com a query fornecida pelo LLM
        results = list(collection.find(query, limit=5))
        
        # Formata os resultados de volta para uma string para o LLM
        return str(results)
    except Exception as e:
        return f"Erro ao executar a consulta no MongoDB: {e}"




# Função de completamento de texto utilizando o model 'groq/llama3-8b-8192'
response = completion(
    model="groq/llama-3.1-8b-instant",
    messages=[
       {"role": "user", "content": "hello from litellm"}
   ],
)

print(response)  # Exibe a resposta do modelo

# Definição do agente "Usuário comum"
market_researcher = Agent(
    role="Usuário comum",  # Função do agente
    goal="Garanta que a busca por um apartamento de aluguel em Jaraguá seja respaldado por pesquisas e dados sólidos gerados dentro do banco de dados utilizado na pesquisa\n"
         "Realize uma pesquisa abrangente e realista com base nas informações nas informações que o usuário inseriu dentro do prompt."
         "Forneça sugestões adequadas de acordo com o orçamento",  # Objetivo do agente
    backstory="O usuário não é um especialista em pesquisa, ele conhece pouco da região, então sugira os melhores imóveis à um custo acessível. O usuário precisa estar satisfeito com o retorno da busca"
              "Você trabalhou com várias startups e empresas estabelecidas.",  # Histórico fictício do agente
    allow_delegation=False,  # O agente não pode delegar tarefas
    verbose=True,  # Exibe informações detalhadas sobre o processo
    llm="groq/llama-3.1-8b-instant"  # Modelo de linguagem usado pelo agente
)


# Definição do agente "corretor imobiliario experiente"
enterpreneur_agent = Agent(
    role="Corretor imobiliário experiente",  # Função do agente
    goal="Crie uma lista com os principais apartamentos na cidade de Jaraguá do Sul que caibam no orçamento do usuário",  # Objetivo
    backstory="Você construiu uma imobiliária de sucesso ao longo dos anos e precisa ajudar o usuário a encontrar o melhor apartamento possível dentro do orçamento."
              "Você tem habilidade de sugerir as melhores ofertas e os clientes sempre fecham negócio com sua imobiliária",  # Histórico fictício
    verbose=True,
    allow_delegation=False,  # Não permite delegação de tarefas
    llm="groq/llama-3.1-8b-instant"  # Modelo de linguagem
)


# Importação da ferramenta para buscas no banco de dados MongoDB
# mongodb_tool = SerperDevTool(
#     llm=ChatGroq(model="groq/llama3-8b-8192"),  # Modelo de linguagem usado pela ferramenta
#     api_key=os.getenv("SERPER_API_KEY"),  # Chave de API para autenticação
#     mongo=os.getenv("DATABASE"),  # Conexão com o MongoDB
# )


mongodb_tool = Tool(
    name="MongoDB_Query_Tool",
    func=query_mongodb,
    description="Útil para buscar e recuperar informações de documentos no MongoDB. "
                "A entrada deve ser uma string de consulta JSON válida, por exemplo: '{\"nome\": \"caneta\"}'"
)



# Definição da tarefa para o Pesquisador de Mercado
task_market_researcher = Task(
    description=(
        "Realizar perguntas caso necssário para entender melhor o apartamento ideal na cidade de Jaraguá do Sul"
        "Verificar se pode achar apartamentos que cabem no orçamento na localização desejada."
        "Avalie e forneça informações pessoais de contato e quanto você tem disponível para gastar mensalmente."
        "Deixe claro que você está procurando um apartamento para alugar, não uma casa, terreno ou qualquer outro tipo de imóvel."
    ),  # Descrição da tarefa
    expected_output=(
        "Um relatório detalhado em português com as melhores opções de apartamentos para alugar em Jaraguá do Sul, que se encaixem no orçamento fornecido."
        "Todas as informações tem que ser dada em português."
    ),  # Saída esperada
    tools=[mongodb_tool],  # Ferramenta usada pela tarefa
    agent=market_researcher,  # Agente que executa a tarefa
)

# Definição da tarefa para o Empreendedor
task_enterpreneur = Task(
    description=(
        "Analise o mercado com o apartamento ideal para o usuário"
        "Estime para verificar se há apartamentos que cabem no orçamento."
        "Avalie a possibilidade nunca sugerir casas, compra de imóveis, terrenos ou qualquer outro tipo de imóvel que não seja apartamento."
        "Forneça as informações necessárias para o corretor imobiliário experiente."
    ),  # Descrição da tarefa
    expected_output=(
        "A saída deve conter os apartamentos mais rentáveis, com melhor custo-benefício, boa localização, segurança e infraestrutura."
        "E uma lista com todos os apartamentos em português e as descrições necessárias que o usuário pedir caso ele peça mais detalhes."
    ),  # Saída esperada
    tools=[mongodb_tool],  # Ferramenta usada
    agent=enterpreneur_agent,  # Agente que executa a tarefa
    output_file='analise-ideia.md'  # Arquivo de saída onde o plano será salvo
)

# Criação do grupo de agentes (Crew) que executará as tarefas
crew = Crew(
    agents=[market_researcher, enterpreneur_agent],  # Agentes envolvidos
    tasks=[task_market_researcher, task_enterpreneur],  # Tarefas atribuídas aos agentes
    verbose=True,  # Exibe informações detalhadas sobre o processo
    max_rpm=25  # Limita o número de requisições por minuto
)

# Execução do Crew com uma ideia de negócio específica: "oversized tshirts in Mumbai India"
result = crew.kickoff(
    inputs={"ideia": "apartamentos em Jaragua do Sul"}  # Ideia fornecida como entrada para as tarefas
)
print(result)  # Exibe o resultado final das tarefas
