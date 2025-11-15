from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from pymongo import MongoClient

import os


class QueryTool(BaseTool):
    name: str = "Selecionar as principais propriedades de Jaraguá do Sul"
    description: str = " Use esta ferramenta para selecionar as principais propriedades de Jaragua do Sul, SC, com base em localização, tipo de propriedade, comodidades e preço. Retorne os resultados como uma string formatada."
   # args_schema: Type[BaseModel] = InsertPropertyInput

    def _run(self) -> str:
        """
        Executa uma consulta no MongoDB para selecionar propriedades com base nos critérios fornecidos.
        """
        try:
            mongo_client = MongoClient(os.getenv("DATABASE"))
            db = mongo_client.get_database("apartamentos")
            collection = db.get_collection("imoveis")
        

            # Executa a busca no MongoDB
            count = 5
            results = collection.find({"cidade": "Jaraguá do Sul"}).limit(count)

            if not results:
                return "Nenhuma propriedade encontrada com os critérios fornecidos."

            # Formata os resultados de volta para uma string
            formatted_results = ",".join([str(result._id) for result in results])
            return formatted_results

        except Exception as e:
            return f"Erro ao executar a consulta no MongoDB: {e}"