from mcp.server.fastmcp import FastMCP
from llm.vector_search import run_aggregation
from pydantic import BaseModel, Field

mcp = FastMCP("Math")

class PropertySearchCriteria(BaseModel):
    tipo: str = Field(
        default="apartamento",
        description="Tipo de apartamento (e.g., studio, apartmento, kitnet)",
        examples=["studio", "apartmento", "kitnet"]
    )
    numerobanhos: int = Field(
        default=1,
        description="Número de banheiros no imóvel",
        examples=[1, 2, 3]
    )
    numeroquartos: int = Field(
        default=1,
        description="Número de quartos no imóvel",
        examples=[1, 2, 3, 4]
    )
    numerosuites: int = Field(
        default=0,
        description="Número de suítes no imóvel",
        examples=[0, 1, 2]
    )
    numerovagas: int = Field(
        default=0,
        description="Número de vagas de garagem",
        examples=[0, 1, 2]
    )
    valor: float = Field(
        default=1000,
        description="Valor do aluguel (em reais)",
        examples=[1500, 2500, 3500]
    )
    areainterna: float = Field(
        default=0,
        description="Área interna em metros quadrados",
        examples=[50, 80, 120]
    )


@mcp.tool() # TOOL CALL BY LLM
# creates the search vector from the data the LLM gives it then runs an aggregation (makes a query) to get good properties
def get_properties(search_term: PropertySearchCriteria) -> list[str]:
    properties =  run_aggregation(search_term.__dict__)

    return [str(property["_id"]) for property in properties] 

if __name__ == "__main__":
    mcp.run(transport="stdio")