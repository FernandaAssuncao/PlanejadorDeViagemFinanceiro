import customtkinter as ctk
from .Agente.AgenteIA import AgenteIA
import re

class Consultor(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.assistente = AgenteIA('Você é um assistente de viagens curto e objetivo.')

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.titulo = ctk.CTkLabel(self, text="Consultor com IA", text_color='#C9A9E6',
                                   fg_color='#1A1A1A',
                                   corner_radius=20, height=60, width=450,
                                   font=('Century Gothic', 25, 'bold'))
        self.titulo.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky='ew')

        self.chat = ctk.CTkScrollableFrame(self, fg_color='#1A1A1A',
                                   border_color='#C9A9E6',
                                   border_width=2,
                                   corner_radius=20)
        self.chat.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky='nsew')
        self.chat.grid_columnconfigure(0, weight=1)

        self.frame_input = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_input.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky='nsew')
        self.frame_input.grid_columnconfigure(0, weight=1)

        self.mensagem = ctk.CTkEntry(self.frame_input, border_width=1,
                                     fg_color='#1A1A1A',
                                     placeholder_text='Digite sua mensagem...',
                                     border_color='#D891EF', corner_radius=50,
                                     height=40)
        self.mensagem.grid(row=0, column=0, padx=(0, 10), sticky='ew')
        self.mensagem.bind('<Return>', lambda event: self.enviar_mensagem())

        self.btn_enviar = ctk.CTkButton(self.frame_input, text="Enviar",
                                        fg_color='#9B59B6', hover_color='#8E44AD',
                                        corner_radius=20, height=40, width=100,
                                        command=self.enviar_mensagem)
        self.btn_enviar.grid(row=0, column=1, sticky='e')

        self.contador_msg = 0

    def __adicionar_mensagem(self, texto, remetente='usuario'):

        msg_container = ctk.CTkFrame(self.chat, fg_color='transparent')

        if remetente == 'usuario':
            bg_color = '#9B59B6'
            anchor_saide = 'e'
        else:
            bg_color = '#2B2B2B'
            anchor_saide = 'w'

        balao = ctk.CTkFrame(msg_container, fg_color=bg_color, corner_radius=15)
        balao.pack(anchor=anchor_saide, padx=0, pady=5)

        label_texto = ctk.CTkLabel(balao,
                                   text=texto,
                                   text_color='#FFFFFF',
                                   font=ctk.CTkFont(size=14),
                                   wraplength=350,
                                   justify='left')
        label_texto.pack(padx=15, pady=10)

        msg_container.grid(row=self.contador_msg, column=0, sticky='nsew', pady=2)
        self.contador_msg += 1

        self.chat._parent_canvas.yview_moveto(1.0)

    def enviar_mensagem(self):
        texto = str(self.mensagem.get().strip())
        if not texto:
            return
        self.__adicionar_mensagem(texto, remetente='usuario')
        self.mensagem.delete(0, 'end')

        resposta_ia_texte = self.assistente(texto)
        resposta = self.__limpar_texto_ia(resposta_ia_texte)
        self.after(500, lambda: self.__adicionar_mensagem(resposta, remetente='ia'))

    @staticmethod
    def __limpar_texto_ia(texto):
        texto_limpo = re.sub(r'\*\*(.*?)\*\*', r'\1', texto)
        texto_limpo = re.sub(r'\*(.*?)\*', r'\1', texto)
        texto_limpo = texto_limpo.strip()
        return texto_limpo
