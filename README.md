# 🏠 Aplicação de Modelos de Linguagem (LLMs) no desenvolvimento de um sistema de busca de apartamentos para aluguel em Jaraguá do Sul/SC

## 1. Descrição geral (objetivo e motivação)
Foi desenvolvido um sistema inteligente, baseado em Modelos de Linguagem de Grande Escala (LLMs), para a busca de imóveis disponíveis para locação no município de Jaraguá do Sul. O sistema terá como finalidade possibilitar a interação em linguagem natural, de modo que o usuário possa expressar suas necessidades habitacionais de forma simples e intuitiva, enquanto a inteligência artificial processa essas informações para realizar buscas mais precisas e personalizadas.

## 2. Motivação
A solução foi desenvolvida para resolver o problema da classificação e busca inteligente de propriedades imobiliárias, motivada pela necessidade de incorporar modelos de linguagem (LLMs) capazes de interpretar preferências de usuários e realizar consultas semânticas de forma autônoma e contextualizada.

## 3. Arquitetura (com diagrama)
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

