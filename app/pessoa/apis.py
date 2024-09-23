# -*- coding: utf-8 -*-
import json
import requests
from app.core.util import get_numbers


def getCityforState(UF) -> list:
    url_api = f'http://servicodados.ibge.gov.br/api/v1/localidades/estados/{UF}/municipios'
    response = requests.get(url_api)
    if response.status_code == 200:
        todos = json.loads(response.content)
        return todos
    return []


def getStates() -> list:
    url_api = 'http://servicodados.ibge.gov.br/api/v1/localidades/estados'
    response = requests.get(url_api)
    if response.status_code == 200:
        todos = json.loads(response.content)
        return todos
    return []


def getDadosCEP(cep):
    """
    "cep": "77023-432",
    "logradouro": "Quadra ARSE 92 Alameda 9",
    "complemento": "",
    "bairro": "Plano Diretor Sul",
    "localidade": "Palmas",
    "uf": "TO",
    "ibge": "1721000",  # mesmo id do models municipios
    "gia": "",
    "ddd": "63",
    """
    url_api = f'https://viacep.com.br/ws/{cep}/json/'
    response = requests.get(url_api)
    if response.status_code == 200:
        dados_json = json.loads(response.content)
        return dados_json
    return None


def getDadosCNPJ(cnpj):
    cnpj = get_numbers(cnpj)
    url_api = f'https://receitaws.com.br/v1/cnpj/{cnpj}'
    response = requests.get(url_api)
    if response.status_code == 200:
        dados_json = json.loads(response.content)
        return dados_json
    return None