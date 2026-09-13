import customtkinter as ctk
from .GerenciadorDeDados.GerenciadorDeDados import GerenciadorDeDados

class Home(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.titulo = ctk.CTkLabel(self, text='Planejador de Viagem Financeiro', text_color='#C9A9E6',
                                   fg_color='#1A1A1A', corner_radius=20,
                                   font=('Century Gothic', 25, 'bold'), height=60, width=450)
        self.titulo.grid(row=0, column=0, columnspan=2, padx=20, pady=20,  sticky='ew')

        self.frame_historico = ctk.CTkFrame(self, fg_color='#1A1A1A', height=60, border_width=2,
                                            border_color='#C9A9E6')
        self.frame_historico.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky='ew')

        self.mensagem = ctk.CTkLabel(self.frame_historico, text='Historico de Buscas de viagens',
                                     text_color='#D891EF', font=('Arial', 12, 'bold'))
        self.mensagem.grid(row=0, column=0, columnspan=1, padx=20, pady=20, sticky='ew')

        self.conteudo_frame = ctk.CTkTextbox(self.frame_historico,
                                             height=100,
                                             fg_color='#1A1A1A',
                                             font=('Arial', 12, 'bold'),
                                             border_color='#D891EF',
                                             border_width=1,
                                             corner_radius=15)
        self.conteudo_frame.grid(row=0, column=1, columnspan=1, padx=20, pady=20, sticky='ew')
        self.frame_historico.columnconfigure(0, weight=1)

        self.mensagem_orcamento_viagens_dias = ctk.CTkLabel(self.frame_historico, text='',
                                                            text_color='#C9A9E6',
                                                            font=('Arial', 12, 'bold'))
        self.mensagem_orcamento_viagens_dias.grid(row=1, column=0, columnspan=1, padx=20, pady=20, sticky='ew')

        self.mensagem_instrucao = ctk.CTkLabel(self, text='Quer começar a analisar sua viagem? Vamos ao planejamento dela então.',
                                               text_color='#F6F3EE', font=('Arial', 12, 'bold'))
        self.mensagem_instrucao.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky='ew')

        self.botao_comecar = ctk.CTkButton(self, text='Começar Planejamento.', text_color='#1A1A1A',
                                           fg_color='#D891EF', border_color='#F6F3EE', border_width=1,
                                           corner_radius=15, hover_color='#C9A9E6', width=60,
                                           command=lambda: self.controller.mostrar_tela('Planejamento'),
                                           font=('Arial', 15, 'bold'))
        self.botao_comecar.grid(row=3, column=0, columnspan=2, padx=20, pady=20, sticky='nsew')

    def colocar_conteudo(self):
        g = GerenciadorDeDados()
        conteudo = g.gerar_conteudo_para_historico()
        self.conteudo_frame.configure(state='normal')
        self.conteudo_frame.delete('0.0', 'end')
        self.conteudo_frame.insert('0.0', conteudo)
        self.conteudo_frame.see('end')
        self.conteudo_frame.configure(state='disabled')
        lista = g.gerar_informacoes_para_a_home()
        self.mensagem_orcamento_viagens_dias.configure(
            text=f'✈️ Viagens: {lista[1]}\n💰 Orçamento planejado: {lista[0]}\n📅 Dias planejados: {lista[2]}',
        )
