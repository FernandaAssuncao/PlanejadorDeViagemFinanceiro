import customtkinter as ctk
from .APIS.Cotacao import Cotacao
from .APIS.Clima import ClimaService
from .GerenciadorDeDados.GerenciadorDeDados import GerenciadorDeDados


class Planejamento(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.cotacao = Cotacao()
        self.clima = ClimaService()
        self.gerenciador = GerenciadorDeDados()

        self.titulo = ctk.CTkLabel(self, text='Planejamento', text_color='#C9A9E6',
                                   fg_color='#1A1A1A', corner_radius=20, height=60,
                                   width=450, font=('Century Gothic', 25, 'bold'))
        self.titulo.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky='ew')

        self.mensagem = ctk.CTkLabel(self, text='Digite o valor que você\n deseja gastar com a viagem.',
                                     text_color='#C9A9E6', font=('Arial', 12, 'bold'))
        self.mensagem.grid(row=1, column=0, padx=20, pady=20, sticky='ew')

        self.campo_valor = ctk.CTkEntry(self, border_width=1, fg_color='#1A1A1A',
                                        border_color='#D891EF',
                                        corner_radius=50)
        self.campo_valor.grid(row=1, column=1, columnspan=1, padx=20, pady=20, sticky='nsew')
        self.campo_valor.bind('<Return>', lambda event: self.campo_pessoas.focus_set())

        self.mensagem2 = ctk.CTkLabel(self, text='Qual sera a quantidade de pessoas?',
                                      text_color='#C9A9E6', font=('Arial', 12, 'bold'))
        self.mensagem2.grid(row=2, column=0, padx=20, pady=20, sticky='ew')

        self.campo_pessoas = ctk.CTkEntry(self, border_width=1, fg_color='#1A1A1A',
                                          border_color='#D891EF', corner_radius=50)
        self.campo_pessoas.grid(row=2, column=1, padx=20, pady=20, sticky='nsew')
        self.campo_pessoas.bind('<Return>', lambda event: self.campo_cidade.focus_set())

        self.mensagem3 = ctk.CTkLabel(self, text='Escolha a moeda do local desejado.',
                                      text_color='#C9A9E6', font=('Arial', 12, 'bold'))
        self.mensagem3.grid(row=3, column=0, padx=20, pady=20, sticky='ew')

        self.moeda_escolhida = ctk.CTkComboBox(self, border_width=1, fg_color='#1A1A1A',
                                               border_color='#D891EF', corner_radius=30,
                                               button_color='#C9A9E6',
                                               values=self.cotacao.moedas_disponiveis)
        self.moeda_escolhida.grid(row=3, column=1, padx=20, pady=20, sticky='nsew')

        self.mensagem4 = ctk.CTkLabel(self, text='Qual o nome da cidade desejada.',
                                      text_color='#C9A9E6', font=('Arial', 12, 'bold'))
        self.mensagem4.grid(row=4, column=0, padx=20, pady=20, sticky='ew')

        self.campo_cidade = ctk.CTkEntry(self, border_width=1, fg_color='#1A1A1A',
                                         border_color='#D891EF', corner_radius=50)
        self.campo_cidade.grid(row=4, column=1, padx=20, pady=20, sticky='nsew')
        self.campo_cidade.bind('<Return>', lambda event: self.campo_dias.focus_set())

        self.mensagem5 = ctk.CTkLabel(self, text='Qual sera a duração da viagem.',
                                      text_color='#C9A9E6', font=('Arial', 12, 'bold'))
        self.mensagem5.grid(row=5, column=0, padx=20, pady=20, sticky='ew')

        self.campo_dias = ctk.CTkEntry(self, border_width=1, fg_color='#1A1A1A',
                                       border_color='#D891EF', corner_radius=50)
        self.campo_dias.grid(row=5, column=1, padx=20, pady=20, sticky='nsew')
        self.campo_dias.bind('<Return>', lambda event: self.planejar_viagem())

        self.resposta = ctk.CTkLabel(self, text='', text_color='#C9A9E6',
                                     font=('Arial', 12, 'bold'))
        self.resposta.grid(row=6, column=0, padx=20, pady=20, sticky='ew')


        self.botao_planejar = ctk.CTkButton(self, text='Planejar Viagem',
                                            border_width=2, fg_color='#C9A9E6',
                                            text_color='#1A1A1A', corner_radius=25,
                                            font=('Arial', 15, 'bold'), hover_color='#6F5A8E',
                                            border_color='#D891EF',
                                            command=self.planejar_viagem)
        self.botao_planejar.grid(row=6, column=1, padx=20, pady=20, sticky='nsew')


    def planejar_viagem(self):
        try:
            valor = float(self.campo_valor.get())
            pessoas = int(self.campo_pessoas.get())
            moeda = str(self.moeda_escolhida.get())
            cidade = str(self.campo_cidade.get())
            dias = int(self.campo_dias.get())
            if valor <= 0:
                raise ValueError('ERRO, O valor da viagem não\n pode ser negativo e nem 0.')
            if pessoas <= 0:
                raise ValueError('ERRO, O numero de pessoas não\n pode ser nagativo e nem 0.')
            if dias <= 0:
                raise ValueError('ERRO, O numero de dias não\n pode ser nagativo e nem 0.')
            if moeda not in self.cotacao.moedas_disponiveis:
                raise ValueError('ERRO, escolha APENAS as moedas disponiveis.')
            if not cidade.strip():
                raise ValueError('Erro, o campo da cidade tem que estar preenchido.')
            self.cotacao.mudar_moeda(moeda)
            valor_moeda = self.cotacao.calcular_valor_para_a_moeda(valor)
            valor_por_pessoa = valor / pessoas
            valor_por_dia = valor / dias
            valor_por_dia_pessoa = valor / pessoas / dias
            buscou = self.clima.buscar_cidade(cidade)
            if buscou:
                resposta = self.clima.gerar_mensagem()
                if not 'valor' in self.controller.dados_viagem or self.controller.dados_viagem.get('cidade') != cidade:
                    self.controller.dados_viagem = {
                        'valor': valor,
                        'pessoas': pessoas,
                        'duracao': dias,
                        'moeda': moeda,
                        'pais': self.clima.pais,
                        'cidade': self.clima.nome_cidade,
                        'simbolo moeda': self.cotacao.simbolo,
                        'conversao': valor_moeda,
                        'valor por pessoa': valor_por_pessoa,
                        'valor por dia': valor_por_dia,
                        'valor por dia e pessoa': valor_por_dia_pessoa,
                        'temperatura': self.clima.temperatura,
                        'sensacao': self.clima.sensacao,
                        'umidade': self.clima.humidade,
                        'condicao': self.clima.condicao,
                        'icone': self.clima.icone,
                    }
                self.mudar_cor_e_mensagem(cor='#7FFFD4',
                                          mensagem='Tudo certo, pode seguir para o resumo.')
                if not 'salvo' in self.controller.dados_viagem:
                    self.gerenciador.salvar_novo_dado(self.controller.dados_viagem)
                    self.controller.dados_viagem['salvo'] = True
                self.controller.mostrar_tela('Resumo')
            else:
                raise ValueError('ERRO, não foi possivel encontrar o clima da cidade.')
        except ValueError as erro:
            cor = '#FF3B30'
            self.mudar_cor_e_mensagem(cor, erro)

    def mudar_cor_e_mensagem(self, cor, mensagem):
        self.resposta.configure(text=mensagem, text_color=cor)
        self.campo_valor.configure(border_color=cor)
        self.campo_pessoas.configure(border_color=cor)
        self.campo_cidade.configure(border_color=cor)
        self.campo_dias.configure(border_color=cor)
