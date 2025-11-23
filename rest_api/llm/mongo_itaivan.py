import requests
import pytz

from config import Settings
from database_connection import get_properties_collection
from datetime import datetime

settings = Settings()
br_timezone = pytz.timezone("America/Sao_Paulo")

MONGO_URI = settings.mongo_uri 
DB_NAME = "apartamentos"
COLLECTION_NAME = "second_test_imoveis"
API_URL = "https://www.itaivan.com/retornar-imoveis-disponiveis"

def collect_informations(pageNumber):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://www.itaivan.com",
        "Referer": "https://www.itaivan.com/aluguel/apartamento/jaragua-do-sul/?&pagina=1&ordenacao=dataatualizacaodesc",
        "X-Requested-With": "XMLHttpRequest",
        "Cookie": "_gcl_au=1.1.38359757.1753560549; _ga=GA1.1.450036994.1743457719; _ga_SJYJ8TD7N6=GS2.1.s1753560549$o14$g1$t1753560847$j60$l0$h0; _ga_XK9SEPS6DH=GS2.1.s1753560548$o13$g1$t1753560847$j60$l0$h0; PHPSESSID=opsamdf3dhaa9tsemq1c7bng9a; _hjSessionUser_6482398=eyJpZCI6ImFkZmI2NDBhLWFiNTQtNWY4YS05OGY2LWNlMDJhNDhhOWRjNCIsImNyZWF0ZWQiOjE3NTQ2MDgwMzc3NTksImV4aXN0aW5nIjp0cnVlfQ==; _hjSession_6482398=eyJpZCI6IjA2MzY4NjZhLWUwMDEtNDFlMi04MjlmLTFjYjZkZTEzNjdiNiIsImMiOjE3NTQ2Njg4ODc5NzgsInMiOjEsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowfQ==",
        "authority": "www.itaivan.com",
        "accept": "*/*",
    }

    # retorno no payload 
    body = {
        "finalidade": "aluguel",
        "codigounidade": "",
        "codigocondominio": 0,
        "codigoproprietario": 0,
        "codigocaptador": 0,
        "codigosimovei": 0,
        "tipos[0][nome]": "Apartamento",
        "tipos[0][codigo]": 2,
        "tipos[0][url_amigavel]": "apartamento",
        "codigocidade": 3,
        "codigoregiao": 0,
        "bairros[0][cidade]": "",
        "bairros[0][codigo]": "",
        "bairros[0][estado]": "",
        "bairros[0][estadoUrl]": "",
        "bairros[0][nome]": "Todos",
        "bairros[0][nomeUrl]": "todos-os-bairros",
        "bairros[0][regiao]": "",
        "endereco": "",
        "edificio": "",
        "numeroquartos": 0,
        "numerovagas": 0,
        "numerobanhos": 0,
        "numerosuite": 0,
        "numerovaranda": 0,
        "numeroelevador": 0,
        "valorde": 0,
        "valorate": 0,
        "areade": 0,
        "areaate": 0,
        "areaexternade": 0,
        "areaexternaate": 0,
        "destaque": 1,
        "opcaoimovel[codigo]": 0,
        "opcaoimovel[nome]": "",
        "opcaoimovel[nomeUrl]": "todas-as-opcoes",
        "codigoOpcaoimovel": 0,
        "retornomapaapp": "false",
        "numeropagina": pageNumber if pageNumber else 1,
        "numeroregistros": 20,
        "ordenacao": "dataatualizacaodesc",
        "codigoempreendimentomae": "",
        "cidades[codigo]": 3,
        "cidades[nome]": "Jaraguá do Sul",
        "cidades[estado]": "SC",
        "cidades[codigoestado]": 24,
        "cidades[nomeurlamigavel]": "jaragua-do-sul",
        "cidades[datahoracadastro]": datetime.now(br_timezone).strftime("%Y-%m-%d %H:%M:%S"), 
        "cidades[nomeUrl]": "jaragua-do-sul",
        "cidades[estadoUrl]": "sc",
        "condominio[codigo]": 0,
        "condominio[nome]": "",
        "condominio[nomeUrl]": "",
        "todos-os-condominios": "",
    }       

    try:
        response = requests.post(API_URL, headers=headers, data=body, timeout=10)
        response.raise_for_status() 

        data = response.json()
        if "lista" in data and isinstance(data["lista"], list):
            return data["lista"]
        else:
            return []
        
    except requests.exceptions.HTTPError as errh:
        print(f" Erro HTTP: {errh}")
        return []

def codigos_already_exist(colecao):
    try:
        codigos = {doc['codigo'] for doc in colecao.find({}, {"codigo": 1, "_id": 0})}
        print(f"Encontrados {len(codigos)} códigos no MongoDB.")
        return codigos
    except Exception as e:
        return set()
    

def new_apart(apartamentos_api, codigos_existentes):
    novos_apartamentos = []
    for apto in apartamentos_api:
        if apto.get("codigo") and apto["codigo"] not in codigos_existentes:
            novos_apartamentos.append(apto)
    
    print(f"Encontrados {len(novos_apartamentos)} novos apartamentos para inserir.")
    return novos_apartamentos

def salvar_novos_no_mongo(novos_apartamentos):
    if not novos_apartamentos:
        print("Itens to insert not found.")
        return
    try:
        colecao = get_properties_collection()

        colecao.insert_many(novos_apartamentos, ordered=False)
        print(f" {len(novos_apartamentos)} new apart was insert on Mongo!")
    except Exception as e:
        print(f"Error to insert new ones {e}")


def aggregate_mongo(aggregation_pipeline):
    if not aggregation_pipeline:
        return None
    try:
        colecao = get_properties_collection()
        
        resultado = colecao.aggregate(aggregation_pipeline)
        return resultado
    
    except Exception as e:
        print(f" Erro ao agregar dados no MongoDB: {e}")
    


