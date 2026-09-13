from dotenv import load_dotenv
import requests
import os

load_dotenv()

class ClimaService:
    def __init__(self):
        self.nome_cidade = None
        self.pais = None
        self.temperatura = None
        self.sensacao = None
        self.humidade = None
        self.descricao = None
        self.icone = None
        self.condicao = None
        self.api_key = os.getenv('API_KEY_CLIMA')
        self.url = 'https://api.openweathermap.org/data/2.5/weather'
        self.icones_clima = {
            'Clear': '☀️',
            'Clouds': '☁️',
            'Rain': '🌧️',
            'Drizzle': '🌦️',
            'Thunderstorm': '⛈️',
            'Snow': '❄️',
            'Mist': '🌫️',
            'Fog': '🌫️',
            'Haze': '🌫️'
        }

    def buscar_cidade(self, cidade:str):
        try:
            params = {
                'q': cidade,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'pt-BR'}
            requisisao = requests.get(self.url, params=params, timeout=10)
            requisisao.raise_for_status()
            dados = requisisao.json()
            self.nome_cidade = dados['name']
            self.pais = dados["sys"]["country"]
            self.temperatura = dados['main']['temp']
            self.sensacao = dados["main"]["feels_like"]
            self.humidade = dados['main']['humidity']
            condicao = dados['weather'][0]['main']
            self.__traduzir_condicao(condicao)
            self.icone = self.icones_clima.get(condicao)
            return True
        except requests.exceptions.HTTPError:
            print('Cidade não encontrada ou chave de API invalida.')
            return False
        except requests.exceptions.ConnectionError:
            print('Erro de conexão com a internet.')
            return False
        except requests.exceptions.Timeout:
            print('Erro, a API não respondeu no tempo certo.')
            return False

    def gerar_mensagem(self):
        if self.temperatura is not None:
            mensagem = '\n'
            mensagem += f'✈️{self.nome_cidade} {self.pais}\n'
            mensagem += f'{self.icone}Condição: {self.condicao}\n'
            mensagem += f'🌡️Temperatura atual {self.temperatura}°C\n'
            mensagem += f'🥵   Sensação: {self.sensacao}°C\n'
            mensagem += f'💧   Umidade: {self.humidade}%\n'
            return mensagem
        else:
            return False

    def __traduzir_condicao(self, condicao):
        if condicao == 'Clear':
            self.condicao = 'Ensolarado'
        elif condicao == 'Clouds':
            self.condicao = 'Nublado'
        elif condicao == 'Rain':
            self.condicao = 'Chuva'
        elif condicao == 'Drizzle':
            self.condicao = 'Garoa'
        elif condicao == 'Thunderstorm':
            self.condicao = 'Tempestade'
        elif condicao == 'Snow':
            self.condicao = 'Neve'
        elif condicao == 'Mist':
            self.condicao = 'Névoa'
        elif condicao == 'Fog':
            self.condicao = 'Nevoeiro'
        elif condicao == 'Haze':
            self.condicao = 'Neblina'
        else:
            self.condicao = None
