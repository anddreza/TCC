# 🏠 Aplicação de Modelos de Linguagem (LLMs) no desenvolvimento de um sistema de busca de apartamentos para aluguel em Jaraguá do Sul/SC

## 1. Descrição geral (objetivo e motivação)
Foi desenvolvido um sistema inteligente, baseado em Modelos de Linguagem de Grande Escala (LLMs), para a busca de imóveis disponíveis para locação no município de Jaraguá do Sul. O sistema terá como finalidade possibilitar a interação em linguagem natural, de modo que o usuário possa expressar suas necessidades habitacionais de forma simples e intuitiva, enquanto a inteligência artificial processa essas informações para realizar buscas mais precisas e personalizadas.

## 2. Motivação
- A solução foi desenvolvida para resolver o problema da classificação e busca inteligente de propriedades imobiliárias, motivada pela necessidade de incorporar modelos de linguagem (LLMs) capazes de interpretar preferências de usuários e realizar consultas semânticas de forma autônoma e contextualizada.
- É combinado  múltiplos agentes de IA (CrewAI + LangChain + Gemini) para interpretar linguagem natural, estruturar consultas e retornar imóveis compatíveis com os critérios fornecidos. O uso do servidor MCP permite modularidade e flexibilidade, enquanto a API centraliza a orquestração do fluxo de dados.

## 3. Arquitetura
A aplicação adota uma arquitetura baseada no Modelo C4, composta pelos seguintes elementos:

- Front-end: React
- Back-end: FastAPI
- Banco de Dados: MongoDB
- IA: LLM + servidor MCP
- Comunicação: HTTP/JSON

## 4. Como rodar o projeto (passo a passo)
#### Pré-requisitos: 
- Node.js
- Python 3.10+
- MongoDB
- Pip ou uv
- Chaves de API (OpenAI, HuggingFace, etc.)

#### Instruções
- Front-end
```
cd front-end
npm install
npm run dev
```
- Backend
```
cd rest_api
pip install -r requirements.txt
uvicorn app.main:app --reload
```

- Variáveis de ambiente

```
Criar um arquivo .env com:
ALLOW_ORIGIN="http://localhost:1234"
MONGO_URI="example_public_mongo_uri"
GOOGLE_API_KEY="example_public_google_api_key"
```

## 5. Implementação
- Render - backend: https://tcc-hx03.onrender.com
- Vercel - frontend: https://tcc-indol-tau.vercel.app/

## 6. Requisitos de Software
#### Requisitos Funcionais(RF): 
```
1. RF001 – O sistema deve permitir que o usuário realize a busca por imóveis utilizando linguagem natural.
2. RF002 – O sistema deve disponibilizar uma interface de navegação que exiba os resultados conforme os critérios solicitados.
3. RF003 – O sistema deve possibilitar que o usuário entre em contato com a imobiliária responsável pelo imóvel, mediante redirecionamento para o número ou canal de contato.
4. RF004 – O sistema deve permitir múltiplas interações, de modo que o usuário possa realizar quantas buscas considerar necessárias.
```
#### Requisitos Não-Funcionais (RNF):
```
1. RNF001 – O sistema deve retornar, no mínimo, um imóvel por consulta realizada.
2. RNF002 – O sistema deve utilizar um LLM de baixo custo operacional e de fácil manutenção (ex.: LLaMA 3 via Groq).
3. RNF003 – A interface deve ser simples, responsiva e acessível via navegador, permitindo a correta visualização das informações em diferentes tamanhos de tela.
```
## 7. Histórico de Decisões
1. Adoção do FastAPI como framework de back-end
Optou-se pelo FastAPI devido à sua elevada performance, suporte nativo a programação assíncrona e forte tipagem baseada em Pydantic. Esses fatores permitiram a construção de uma API robusta, com validação automática de dados, documentação integrada e baixo tempo de resposta, aspectos essenciais para uma aplicação que integra modelos de IA e operações de busca vetorial.

2. Utilização de um LLM para processamento semântico
A escolha de empregar um modelo de linguagem (LLM) foi motivada pela necessidade de interpretar preferências dos usuários de forma contextual e realizar transformações semânticas que possibilitam consultas mais precisas. O LLM atua como componente central na geração do vetor de busca, na extração de intenções e na coordenação entre agentes internos.

3. Introdução do servidor MCP como ponte entre a API e ferramentas externas
O servidor MCP foi adotado como mecanismo facilitador da comunicação entre o LLM e as ferramentas responsáveis por executar tarefas específicas, como a geração de vetores de busca e a execução de agregações no banco de dados. Essa abordagem modular melhora a escalabilidade, permitindo a adição de novas capacidades sem alterar o núcleo da aplicação.

4. Definição de um pipeline de busca baseado em agregações
A realização da consulta às propriedades por meio de agregações foi escolhida por oferecer maior flexibilidade na definição de etapas de busca, filtragem e seleção de campos retornados. Essa arquitetura permite otimizar a precisão da recomendação e ajustar os critérios conforme a evolução do projeto.

5. Padronização da comunicação entre componentes via JSON/HTTP
Estabeleceu-se que a comunicação entre o front-end, API, LLM e MCP ocorreria por meio de requisições HTTP utilizando JSON como formato de troca. A decisão prioriza interoperabilidade, simplicidade e compatibilidade com diferentes tecnologias e ambientes de implantação.

## 8. Modelagem 
### Caso de Uso
```
Caso de Uso 1 — Buscar imóveis para locação

Ator principal: Usuário Objetivo: Consultar imóveis disponíveis conforme preferências. 
Fluxo principal:
Usuário insere comandos em linguagem natural.
Sistema interpreta critérios (ex.: preço, localização, número de quartos).
Sistema recupera dados da base.
Sistema apresenta lista filtrada ao usuário.
```

```
####  Caso de Uso 2 — Atualização automática da base de imóveis

Ator principal: Sistema Objetivo: Atualizar periodicamente os imóveis disponíveis. 
Fluxo principal:
Sistema acessa API da imobiliária.
Dados são extraídos e validados.
Registros desatualizados são removidos.
Banco é atualizado.
```

```
#### Caso de Uso 3 — Interação com o LLM

Ator principal: Sistema Objetivo: Interpretar solicitações feitas em linguagem natural. 
Fluxo principal:
Comando do usuário é enviado ao LLM Gemini.
LLM interpreta e converte para parâmetros estruturados.
Sistema executa consulta com base na interpretação.
```
## 9. BPMN (Descrição textual)
- Usuário → envia comando → Frontend
- Frontend → envia requisição → API FastAPI
- API → envia texto → LLM Gemini
- LLM → retorna parâmetros → Servidor MCP
- Servidor MCP → executa busca → Banco de Dados
- Banco → retorna resultados → MCP → API → Frontend

## 10. Diagrama de arquitetura
#### Nível 1 — Diagrama de Contexto

O sistema recebe comandos do usuário, interpreta via LLM Gemini, consulta o banco por meio do MCP e retorna resultados para o usuário.

#### Nível 2 — Diagrama de Containers

Frontend (React): interface
API (FastAPI): orquestra chamadas
LLM Gemini: interpretação semântica
Servidor MCP: execução de ferramentas
Banco de Dados: armazenamento e atualização diária

####  Nível 3 — Componentes

- Componente de Rotas: /properties
- Componente de Interpretação: agente LLM
- Componente de Busca: ferramenta get_properties
- Componente de Atualização: rotina diária da API

####  Nível 4 — Código

- api/routes/user_routes.py – rotas de usuário
- api/services/user_service.py – regras de negócio
- api/models/user_model.py – modelo de dados
- frontend/src/pages/Home.jsx – tela inicial
- frontend/src/services/api.js – comunicação com API