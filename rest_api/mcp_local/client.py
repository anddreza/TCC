from openai import OpenAI
from mcp.client import Client

# Inicializa cliente LLM
client = OpenAI(GROQ_API_KEY="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")

# Cria cliente MCP e conecta ao seu servidor
mcp = Client("http://localhost:8080")

# Registra o MCP no contexto do modelo
client.register_context_server(mcp)

# Envia prompt
response = client.responses.create(
    model="gpt-4.1",
    input=[{"role": "user", "content": "Liste os usuários no banco MongoDB"}]
)

print(response.output_text)

