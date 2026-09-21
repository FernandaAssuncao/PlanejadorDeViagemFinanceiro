import requests

class Cotacao:
    def __init__(self):
        self.__cotacao_moeda = 0
        self.__moeda = None
        self.moedas_disponiveis = []
        self.__listas_moedas = {}
        self.__simbolo = None
        self.__link = 'https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL'
        self.__pegar_moeda()

    def __pegar_moeda(self):
        try:
            requisicao = requests.get(self.__link, timeout=10)
            requisicao.raise_for_status()
            dic = requisicao.json()
            for sigla, dados in dic.items():
                self.moedas_disponiveis.append(sigla)
                self.__listas_moedas[sigla] = float(dados['bid'])
        except requests.exceptions.Timeout:
            print('ERRO, API demorou demais para responder.')
        except requests.exceptions.HTTPError as error:
            print(f'Erro HTTP: {error}')
        except requests.exceptions.ConnectionError:
            print('Erro de conexão.')

    def calcular_valor_para_a_moeda(self, valor):
        return valor / self.cotacao

    def mudar_moeda(self, moeda):
        self.moeda = moeda

    @property
    def simbolo(self):
        return self.__simbolo

    @simbolo.setter
    def simbolo(self, moeda):
        if moeda == 'USDBRL':
            self.__simbolo = '$'
        elif moeda == 'EURBRL':
            self.__simbolo = '€'
        elif moeda == 'BTCBRL':
            self.__simbolo = '₿'

    @property
    def moeda(self):
        return self.__moeda

    @moeda.setter
    def moeda(self, moeda):
        if moeda in self.moedas_disponiveis:
            self.__moeda = moeda
            self.cotacao = self.__listas_moedas[moeda]
            self.simbolo = moeda
        else:
            raise ValueError("ERRO, moeda não disponivel.")

    @property
    def cotacao(self):
        return self.__cotacao_moeda

    @cotacao.setter
    def cotacao(self, cotacao):
        self.__cotacao_moeda = cotacao

if __name__ == '__main__':
    cotacao = Cotacao()
    cotacao.mudar_moeda('EURBRL')
    print(cotacao.moeda)
    print(cotacao.cotacao)
