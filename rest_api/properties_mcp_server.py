from mcp.server.fastmcp import FastMCP
from llm.vector_search import run_aggregation
from pydantic import BaseModel, Field

mcp = FastMCP("Math")

search_term_1 = {
    "tipo": "Apartamento",
    "numerobanhos": 2,
    "numeroquartos": 3,
    "numerosuites": 1, 
    "numerovagas": 2,
    "valor": 2500,
    "areainterna": 120
}

class PropertySearchCriteria(BaseModel):
    tipo: str = Field(
        ...,
        description="Tipo de apartamento (e.g., studio, apartmento, kitnet)",
        examples=["studio", "apartmento", "kitnet"]
    )
    numerobanhos: int = Field(
        ...,
        description="Número de banheiros no imóvel",
        examples=[1, 2, 3]
    )
    numeroquartos: int = Field(
        ...,
        description="Número de quartos no imóvel",
        examples=[1, 2, 3, 4]
    )
    numerosuites: int = Field(
        ...,
        description="Número de suítes no imóvel",
        examples=[0, 1, 2]
    )
    numerovagas: int = Field(
        ...,
        description="Número de vagas de garagem",
        examples=[0, 1, 2]
    )
    valor: float = Field(
        ...,
        description="Valor do aluguel (em reais)",
        examples=[1500, 2500, 3500]
    )
    areainterna: float = Field(
        ...,
        description="Área interna em metros quadrados",
        examples=[50, 80, 120]
    )


@mcp.tool()
def get_properties(search_term: PropertySearchCriteria) -> list[str]:
    properties =  run_aggregation(search_term.__dict__)

    return [str(property["_id"]) for property in properties] 
#    return ['68d03e0f1f6b16923112cc1c']

if __name__ == "__main__":
    mcp.run(transport="stdio")