import customtkinter as ctk

class Resumo(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.titulo = ctk.CTkLabel(self, text='Resumo da Viagem', text_color='#C9A9E6',
                                   fg_color='#1A1A1A', corner_radius=20,
                                   width=450, height=60,
                                   font=('Century Gothic', 25, 'bold'))
        self.titulo.grid(row=0, column=0, columnspan=2, padx=20, pady=20,sticky='ew')

        self.cidade = ctk.CTkLabel(self, text='Nenhuma Viagem planejada', text_color='#C9A9E6',
                                   font=('Segoe UI', 15, 'bold'))
        self.cidade.grid(row=1, column=0, columnspan=1, padx=20, pady=20, sticky='ew')

        self.orcamento = ctk.CTkLabel(self, text='', text_color='#C9A9E6',
                                      font=('Segoe UI', 15, 'bold'))
        self.orcamento.grid(row=2, column=0, columnspan=1, padx=20, pady=20, sticky='ew')

        self.viajantes = ctk.CTkLabel(self, text='', text_color='#C9A9E6',
                                      font=('Segoe UI', 15, 'bold'))
        self.viajantes.grid(row=2, column=1, columnspan=1, padx=20, pady=20, sticky='ew')

        self.conversao = ctk.CTkLabel(self, text='', text_color='#C9A9E6',
                                      font=('Segoe UI', 15, 'bold'))
        self.conversao.grid(row=3, column=0, columnspan=1, padx=20, pady=20, sticky='ew')

        self.orcamento_por_pessoa = ctk.CTkLabel(self, text='', text_color='#C9A9E6',
                                                 font=('Segoe UI', 15, 'bold'))
        self.orcamento_por_pessoa.grid(row=3, column=1, columnspan=1, padx=20, pady=20, sticky='ew')

        self.orcamento_por_dia = ctk.CTkLabel(self, text='', text_color='#C9A9E6',
                                              font=('Segoe UI', 15, 'bold'))
        self.orcamento_por_dia.grid(row=4, column=0, columnspan=1, padx=20, pady=20, sticky='ew')

        self.orcamento_por_pessoa_dia = ctk.CTkLabel(self, text='', text_color='#C9A9E6',
                                                     font=('Segoe UI', 15, 'bold'))
        self.orcamento_por_pessoa_dia.grid(row=4, column=1, columnspan=1, padx=20, pady=20, sticky='ew')

        self.titulo_clima = ctk.CTkLabel(self, text='🌤️ CLIMA', text_color='#C9A9E6',
                                         font=('Segoe UI', 15, 'bold'))
        self.titulo_clima.grid(row=5, column=0, columnspan=1, padx=20, pady=20, sticky='ew')

        self.temperatura = ctk.CTkLabel(self, text='', text_color='#C9A9E6',
                                        font=('Segoe UI', 15, 'bold'))
        self.temperatura.grid(row=5, column=1, columnspan=1, padx=20, pady=20, sticky='ew')


    def atualizar_resumo(self):
        dados = self.controller.dados_viagem

        if not dados:
            return

        self.cidade.configure(text=f'📍 {dados["cidade"]} {dados["pais"]}')
        self.orcamento.configure(text=f'💰 Orcamento R${dados["valor"]:.2f}')
        self.viajantes.configure(text=f'👥 Viajantes: {dados["pessoas"]}\n 📅 Duração: {dados["duracao"]}')
        self.conversao.configure(text=f'💱 Conversao: {dados["simbolo moeda"]}{dados["conversao"]:.2f}')
        self.orcamento_por_pessoa.configure(text=f'Orçamento por\n pessoas: R${dados["valor por pessoa"]:.2f}')
        self.orcamento_por_dia.configure(text=f'Orçamento por\n dia: R${dados["valor por dia"]:.2f}')
        self.orcamento_por_pessoa_dia.configure(text=f'Orçamento por dia\n e pessoa: R${dados["valor por dia e pessoa"]:.2f}')
        self.temperatura.configure(text=(
            f'{dados["icone"]} {dados["condicao"]}\n'
            f'🌡️ Temperatura: {dados["temperatura"]}°C\n'
            f'🥵 Sensação: {dados["sensacao"]}°C\n'
            f'💧 umidade: {dados["umidade"]}%'
        ))
