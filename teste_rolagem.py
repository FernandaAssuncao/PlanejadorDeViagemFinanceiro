import customtkinter as ctk


class ChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Chat com IA - Consultor")
        self.geometry("600x500")

        self.COLOR_BG = "#212121"
        self.COLOR_USER_MSG = "#9B59B6"  # Seu roxo original para suas mensagens
        self.COLOR_AI_MSG = "#2B2B2B"  # Cinza escuro para as mensagens da IA
        self.COLOR_TEXT = "#FFFFFF"

        self.configure(fg_color=self.COLOR_BG)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 1. Container principal do Chat com rolagem (Scrollable Frame)
        self.chat_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.chat_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nsew")
        self.chat_frame.grid_columnconfigure(0, weight=1)

        # 2. Frame inferior para o Input e Botão de Enviar
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        # Campo de digitação
        self.entry_msg = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Digite sua mensagem...",
            height=40,
            corner_radius=20,
            font=ctk.CTkFont(size=14)
        )
        self.entry_msg.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        self.entry_msg.bind("<Return>", lambda event: self.enviar_mensagem())  # Envia com Enter

        # Botão Enviar
        self.btn_enviar = ctk.CTkButton(
            self.input_frame,
            text="Enviar",
            width=80,
            height=40,
            corner_radius=20,
            fg_color="#9B59B6",
            hover_color="#8E44AD",
            command=self.enviar_mensagem
        )
        self.btn_enviar.grid(row=0, column=1)

        # Variável para controlar as linhas do grid do chat
        self.msg_counter = 0

        # Mensagem inicial da IA de exemplo
        self.adicionar_mensagem("Olá! Sou seu consultor de viagens. Como posso ajudar?", remetente="ia")

    def adicionar_mensagem(self, texto, remetente="usuario"):
        # Frame individual para a mensagem (para alinhar à esquerda ou direita)
        msg_container = ctk.CTkFrame(self.chat_frame, fg_color="transparent")

        # Define a cor do balão e o alinhamento dependendo de quem mandou
        if remetente == "usuario":
            bg_color = self.COLOR_USER_MSG
            anchor_side = "e"  # Direita
            padx_val = (50, 10)
        else:
            bg_color = self.COLOR_AI_MSG
            anchor_side = "w"  # Esquerda
            padx_val = (10, 50)

        # O balão da mensagem em si
        balao = ctk.CTkFrame(msg_container, fg_color=bg_color, corner_radius=15)
        balao.pack(anchor=anchor_side, padx=0, pady=5)

        # Texto dentro do balão
        label_texto = ctk.CTkLabel(
            balao,
            text=texto,
            text_color=self.COLOR_TEXT,
            font=ctk.CTkFont(size=14),
            wraplength=350,  # Quebra a linha se o texto for muito longo
            justify="left"
        )
        label_texto.pack(padx=15, pady=10)

        # Posiciona o container da mensagem na tela principal do chat
        msg_container.grid(row=self.msg_counter, column=0, sticky="ew", pady=2)
        self.msg_counter += 1

        # Rola automaticamente para a última mensagem
        self.chat_frame._parent_canvas.yview_moveto(1.0)

    def enviar_mensagem(self):
        texto_usuario = self.entry_msg.get().strip()
        if not texto_usuario:
            return  # Não envia mensagem vazia

        # Adiciona a mensagem do usuário na tela
        self.adicionar_mensagem(texto_usuario, remetente="usuario")
        self.entry_msg.delete(0, "end")

        # Simula uma resposta da IA (Aqui você integraria com o seu modelo KNN ou API)
        resposta_ia = f"Entendi! Analisando sua solicitação sobre: '{texto_usuario}'..."
        self.after(500, lambda: self.adicionar_mensagem(resposta_ia, remetente="ia"))


if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()
