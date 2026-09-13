import customtkinter as ctk
from .HomeFrame import Home
from .Planejamento import Planejamento
from .Consultor import Consultor
from .Resumo import Resumo


class InterfacePrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Planejador de Viagem Financeiro. ')
        self.geometry('750x600')
        self._set_appearance_mode('dark')

        self.dados_viagem = {}

        self.grid_rowconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.menu = ctk.CTkFrame(self, fg_color='#1A1A1A', border_color='#C9A9E6',
                                 border_width=1)
        self.menu.grid(row=0, column=0, rowspan=5, padx=(20, 10), pady=(20, 10), sticky='nsew')

        self.texto_menu = ctk.CTkLabel(self.menu, text='MENU', text_color='#6F5A8E',
                                       font=('Arial', 18, 'bold'))
        self.texto_menu.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')

        self.botao_home = ctk.CTkButton(self.menu, text='🏠 Home', fg_color='#1A1A1A',
                                        border_color='#C9A9E6', border_width=2,
                                        corner_radius=1, hover_color='#A88BD6',
                                        command=lambda: self.mostrar_tela('Home'))
        self.botao_home.grid(row=1, column=0, padx=20, pady=20, sticky='nsew')

        self.botao_planejamento = ctk.CTkButton(self.menu, text='✈️Planejamento', fg_color='#1A1A1A',
                                                border_color='#C9A9E6', corner_radius=1,
                                                border_width=2, hover_color='#A88BD6',
                                                command=lambda: self.mostrar_tela('Planejamento'))
        self.botao_planejamento.grid(row=2, column=0, padx=20, pady=20, sticky='nsew')

        self.botao_resumo = ctk.CTkButton(self.menu, text='📊 Minha Viagem', fg_color='#1A1A1A',
                                          border_color='#C9A9E6', corner_radius=1,
                                          border_width=2, hover_color='#A88BD6',
                                          command=lambda: self.mostrar_tela('Resumo'))
        self.botao_resumo.grid(row=3, column=0, padx=20, pady=20, sticky='nsew')

        self.botao_consultor = ctk.CTkButton(self.menu, text='🤖 Consultor IA', fg_color='#1A1A1A',
                                             border_color='#C9A9E6', border_width=2,
                                             corner_radius=1, hover_color='#A88BD6',
                                             command=lambda: self.mostrar_tela('Consultor'))
        self.botao_consultor.grid(row=4, column=0, padx=20, pady=20, sticky='nsew')


        self.container = ctk.CTkFrame(self)
        self.container.grid(row=0, column=1, padx=(10, 20), pady=(10, 20), sticky='nsew')
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for TelasClasse in (Home, Planejamento, Consultor, Resumo):
            nome_tela = TelasClasse.__name__
            frame = TelasClasse(parent=self.container, controller=self)
            self.frames[nome_tela] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.mostrar_tela('Home')

    def mostrar_tela(self, nome_tela):
        frame = self.frames[nome_tela]
        if nome_tela == 'Resumo':
            frame.atualizar_resumo()
        if nome_tela == 'Home':
            frame.colocar_conteudo()
        frame.tkraise()
