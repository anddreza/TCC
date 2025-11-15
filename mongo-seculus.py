import requests
from pymongo import MongoClient
from dotenv import load_dotenv


# 🔹 Configurações
MONGO_URI = "mongodb+srv://anddrezas:pwd123@cluster0.xhwszy1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  
DB_NAME = "apartamentos"
COLLECTION_NAME = "imoveis"
API_URL = "https://www.seculus.net/imoveis/ajax/"

def coletar_dados():
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        # "Accept": "application/json",
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
        "numeropagina": 1,
        "numeroregistros": 20,
        "ordenacao": "dataatualizacaodesc",
        "codigoempreendimentomae": "",
        "cidades[codigo]": 3,
        "cidades[nome]": "Jaraguá do Sul",
        "cidades[estado]": "SC",
        "cidades[codigoestado]": 24,
        "cidades[nomeurlamigavel]": "jaragua-do-sul",
        "cidades[datahoracadastro]": "2025-08-01 16:58:01", 
        "cidades[nomeUrl]": "jaragua-do-sul",
        "cidades[estadoUrl]": "sc",
        "condominio[codigo]": 0,
        "condominio[nome]": "",
        "condominio[nomeUrl]": "",
        "todos-os-condominios": "",

    }       
    
    
#     try:
#         # A API precisa de uma lista de imóveis.
#         response = requests.post(API_URL, headers=headers, timeout=10, data=body)
#         response.raise_for_status() 
        
#         # A resposta é um dicionário, mas o insert_many precisa de uma lista.
#         # Ajustamos o retorno para garantir que seja uma lista.
#         data = response.json()
#         if "imoveis" in data and isinstance(data["imoveis"], list):
#             return data["imoveis"]
#         else:
#             print("⚠ Resposta da API não contém a lista 'imoveis'.")
#             return []
            


# def salvar_no_mongo(dados):
#     cliente = MongoClient(MONGO_URI)
#     db = cliente[DB_NAME]
#     colecao = db[COLLECTION_NAME]

#     # 🔹 Limpa dados antigos
#     colecao.delete_many({})
    
#     if dados:
#         colecao.insert_many(dados)
#         print(f"✅ {len(dados)} registros inseridos no MongoDB.")
#     else:
#         print("⚠ Nenhum dado para inserir.")

# if __name__ == "__main__":
#     print("Coletando dados da API...")
#     dados = coletar_dados()
#     salvar_no_mongo(dados)


    try:
        print("Fazendo requisição para a API...")
        response = requests.post(API_URL, headers=headers, data=body, timeout=10)
        
        # resposta
        print(f"Status Code da resposta: {response.status_code}")
        response.raise_for_status() # 200 (OK)

        
        # requisição no formato JSON, que é mais legível.
        # print("\n✅ Requisição bem-sucedida! Conteúdo da resposta:")
        # print(response.json())
        
        # Ajustamos o retorno para garantir que seja uma lista.
        data = response.json()
        if "lista" in data and isinstance(data["lista"], list):
            return data["lista"]
        else:
            print("⚠ Resposta da API não contém a lista 'imoveis'.")
            return []
        
    except requests.exceptions.HTTPError as errh:
        print(f" Erro HTTP: {errh}")
        return []
    except requests.exceptions.ConnectionError as errc:
        print(f" Erro de Conexão: {errc}")
        return []
    except requests.exceptions.Timeout as errt:
        print(f" Timeout da Requisição: {errt}")
        return []
    except requests.exceptions.RequestException as err:
        print(f" Ocorreu um erro na requisição: {err}")
        return []
    except Exception as e:
        print(f" Erro ao coletar dados: {e}")
        return []

## tem que verificar o código existente, porém não é possível de mapear conforme os codigos? 
def get_codigos_existentes(colecao):
    try:
        codigos = {doc['codigo'] for doc in colecao.find({}, {"codigo": 1, "_id": 0})}
        print(f"✅ Encontrados {len(codigos)} códigos no MongoDB.")
        return codigos
    except Exception as e:
        print(f"❌ Erro ao buscar códigos no MongoDB: {e}")
        return set()
    

def filtrar_novos_apartamentos(apartamentos_api, codigos_existentes):
    novos_apartamentos = []
    for apto in apartamentos_api:
        # Certifique-se de que a chave 'codigo' existe e o valor não é None
        if apto.get("codigo") and apto["codigo"] not in codigos_existentes:
            novos_apartamentos.append(apto)
    
    print(f"✅ Encontrados {len(novos_apartamentos)} novos apartamentos para inserir.")
    return novos_apartamentos

def salvar_novos_no_mongo(novos_apartamentos):
    if not novos_apartamentos:
        print("⚠ Nenhum novo apartamento para inserir.")
        return
    try:
        cliente = MongoClient(MONGO_URI)
        db = cliente[DB_NAME]
        colecao = db[COLLECTION_NAME]

        colecao.insert_many(novos_apartamentos)
        print(f"✅ {len(novos_apartamentos)} novos apartamentos inseridos no MongoDB com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao inserir dados no MongoDB: {e}")

# def salvar_no_mongo(dados):
#     cliente = MongoClient(MONGO_URI)
#     db = cliente[DB_NAME]
#     colecao = db[COLLECTION_NAME]

#     colecao.delete_many({})
    
#     if dados:
#         colecao.insert_many(dados)
#         print(f"✅ {len(dados)} registros inseridos no MongoDB.")
#     else:
#         print("⚠ Nenhum dado para inserir.")


if __name__ == "__main__":
    coletar_dados()
    dados = coletar_dados()
    salvar_novos_no_mongo(dados)
