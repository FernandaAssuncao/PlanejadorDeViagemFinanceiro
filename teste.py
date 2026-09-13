import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY_CLIMA")

url = 'https://api.openweathermap.org/data/2.5/weather'
params = {
    'q': 'São Paulo',
    'appid': api_key,
    'units': 'metric',
    'lang': 'pt-BR'
}

resposta = requests.get(url, params=params, timeout=5)
dados = resposta.json()
print(dados)
nome_cidade = dados["name"]
pais = dados["sys"]["country"]
temperatura = dados["main"]["temp"]
sensacao = dados["main"]["feels_like"]
humidade = dados["main"]["humidity"]
descricao = dados["weather"][0]["description"]
print(nome_cidade)
print(pais)
print(temperatura)
print(sensacao)
print(humidade)
print(descricao)
