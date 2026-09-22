import pandas as pd
from datetime import datetime
import os

class GerenciadorDeDados:
    nome_arquivo = 'data/Historico_de_viagens.csv'

    def __criar_arquivo(self):
        if not os.path.exists(self.nome_arquivo):
            df = pd.DataFrame(columns=[
                'ID',
                'Data',
                'Cidade',
                'Pais',
                'Orcamento',
                'Pessoas',
                'Moeda',
                'Dias',
                'Valor convertido',
                'Valor por pessoa',
                'Valor por dia',
                'Temperatura',
                'Condicao'
            ])
            df.to_csv(self.nome_arquivo, index=False)

    def salvar_novo_dado(self, dados):
        if not os.path.exists(self.nome_arquivo):
            self.__criar_arquivo()
        data = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        df = pd.read_csv(self.nome_arquivo)
        total = len(df)
        id = total + 1
        nova_linha = pd.DataFrame([{
            'ID': id,
            'Data': data,
            'Cidade': dados['cidade'],
            'Pais': dados['pais'],
            'Orcamento': dados['valor'],
            'Pessoas': dados['pessoas'],
            'Moeda': dados['moeda'],
            'Dias': dados['duracao'],
            'Valor convertido': dados['conversao'],
            'Valor por pessoa': dados['valor por pessoa'],
            'Valor por dia': dados['valor por dia'],
            'Temperatura': dados['temperatura'],
            'Condicao': dados['condicao']
        }])
        nova_linha.to_csv(self.nome_arquivo, mode='a', index=False, header=False)
        return True

    def gerar_conteudo_para_historico(self):
        if not os.path.exists(self.nome_arquivo):
            self.__criar_arquivo()
        texto = ''
        df = pd.read_csv(self.nome_arquivo)
        dados = df.to_dict(orient='records')
        for viagem in dados:
            texto += f'Cidade: {viagem["Cidade"]}\nPaís: {viagem["Pais"]}\nOrçamento: {viagem["Orcamento"]}\n'
            texto += f'{"-" * 20}\n'
        return texto

    def gerar_informacoes_para_a_home(self):
        if not os.path.exists(self.nome_arquivo):
            self.__criar_arquivo()
        df = pd.read_csv(self.nome_arquivo)
        orcamento = df['Orcamento'].sum().item()
        viagens = len(df)
        dias = df['Dias'].sum().item()
        return [orcamento, viagens, dias]

    def gerar_historico_para_ia(self):
        if not os.path.exists(self.nome_arquivo):
            self.__criar_arquivo()
        df = pd.read_csv(self.nome_arquivo)
        dados = df.to_dict(orient='records')
        return dados
