import customtkinter as ctk
from .Agente.AgenteIA import AgenteIA
from .APIS.Cotacao import Cotacao
from .APIS.Clima import ClimaService
from .GerenciadorDeDados.GerenciadorDeDados import GerenciadorDeDados
from langchain_core.tools import tool
import threading
import re
import json

class Consultor(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        @tool
        def pegar_informacoes_viagem_usuario_atualmente_planejada() -> str:
            """Retorna SOMENTE a viagem atualmente planejada pelo usuario no aplicativo.

            Use esta ferramenta quando o usuario perguntar sobre a viagem que ele
            está planejando agora, como destino, orçamento, quantidade de pessoas,
            quantidade de dias, moeda ou outras informações da viagem atual.
            Esta ferramenta NÃO retorna o historico de viagens anteriores."""
            dados = self.controller.dados_viagem
            if not dados:
                return f'Não foi encontrada nenhuma viagem planejada pelo usuario.'
            else:
                return f'As informação da viagem planejada pelo usuario são: {json.dumps(self.controller.dados_viagem, indent=2, ensure_ascii=False)}'

        @tool
        def pegar_cotacao_moeda(moeda:str) -> str:
            """Pega a cotação da moeda que o usuario quer saber e retorna o valor dela em real
            A variavel necessesaria é a moeda que o usuario pediu, por exemplo euro, ou dolár."""
            moeda = moeda.strip().lower()
            cotacao = Cotacao()
            if moeda == 'euro':
                cotacao.mudar_moeda('EURBRL')
                return f'A cotação da moeda {cotacao.moeda} é R${cotacao.cotacao:.2f}'
            elif moeda == 'dólar':
                cotacao.mudar_moeda('USDBRL')
                return f'A cotação da moeda {cotacao.moeda} é R${cotacao.cotacao:.2f}'
            elif moeda == 'biticoin':
                cotacao.mudar_moeda('BTCBRL')
                return f'A cotação da moeda {cotacao.moeda} é R${cotacao.cotacao:.2f}'
            else:
                return 'Moeda não encontrada.'

        @tool
        def pegar_clima_cidade(cidade:str) -> str:
            """"Busca o clima da cidade que o usuario perguntou e retorna por exemplo:
            temperatura, humidade, sensação, condição. E a função precisa do nome da cidade
            que o usuario deseja: Ex: Berlim."""
            cidade = cidade.strip().lower()
            clima = ClimaService()
            buscou = clima.buscar_cidade(cidade=cidade)
            if buscou:
                return f'A temperatura da cidade é {clima.temperatura}°C. A umidade da cidade é {clima.humidade}% A condição é {clima.condicao} e a sensação é de {clima.sensacao}'
            else:
                return 'Não foi possivel buscar a cidade que o usuario quer.'

        @tool
        def pegar_historico_de_viagens_planejadas_pelo_usuario() -> list:
            """Retorna o historico de viagens que o usuario já planejou anteriormente.
            Use esta ferramenta SOMENTE quando o usuario perguntar sobre viagens
            anteriores, historico, viagens passadas, destinos já planejados ou
            quiser comparar suas viagens anteriores.
            Esta ferramenta NÃO representa a viagem atualmente planejada."""
            c = GerenciadorDeDados()
            dados = c.gerar_historico_para_ia()
            if dados:
                return dados
            else:
                return [{'Dados':
                             'Não a dados para mostrar. O usuario não realizou nenhuma busca.'}]

        self.ferramentas = [pegar_informacoes_viagem_usuario_atualmente_planejada,
                            pegar_cotacao_moeda,
                            pegar_clima_cidade,
                            pegar_historico_de_viagens_planejadas_pelo_usuario]
        self.assistente = AgenteIA('''
            Você é um assistente de viagens curto e objetivo.

            Existem duas fontes diferentes de informações sobre viagens:

            1. VIAGEM ATUALMENTE PLANEJADA:
           Representa somente a viagem que está atualmente planejada
           no aplicativo pelo usuário.
           Use a ferramenta pegar_informacoes_viagem_usuario_atualmente_planejada quando
           o usuário perguntar sobre a viagem atual.

            2. HISTÓRICO DE VIAGENS:
            Representa viagens planejadas anteriormente pelo usuário.
            Use a ferramenta pegar_historico_de_viagens somente quando
            o usuário perguntar sobre viagens anteriores, histórico,
            viagens passadas ou comparações entre viagens.
            Nunca confunda a viagem atualmente planejada com o histórico.
            Se o usuário disser "minha viagem", "minha viagem atual",
            "a viagem que estou planejando" ou fizer uma pergunta sobre
            o planejamento atual, consulte a viagem atualmente planejada.
            Se o usuário disser "minhas viagens anteriores", "histórico",
            "viagens que já fiz/planejei", "viagens passadas" ou pedir
            comparação com viagens anteriores, consulte o histórico.
            Se o usuário atualizar a viagem no aplicativo, consulte novamente
            a ferramenta da viagem atualmente planejada para obter os dados
            atualizados.
            Se você já possui uma informação que continua válida na conversa,
            não chame novamente a ferramenta desnecessariamente.
            Responda de forma curta e objetiva.''', ferramentas=self.ferramentas)

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

        self.mensagem.configure(state="disabled")
        self.configure(cursor="watch")

        def processar_ia_no_segundo_plano():
            resposta_ia_texte = self.assistente(texto)

            resposta = self.__limpar_texto_ia(resposta_ia_texte)
            self.after(500, lambda: self.__adicionar_mensagem(resposta, remetente='ia'))

            self.configure(cursor="")
            self.mensagem.configure(state="normal")

        thread = threading.Thread(target=processar_ia_no_segundo_plano, daemon=True)
        thread.start()

    @staticmethod
    def __limpar_texto_ia(texto):
        texto_limpo = re.sub(r'\*\*(.*?)\*\*', r'\1', texto)
        texto_limpo = re.sub(r'\*(.*?)\*', r'\1', texto)
        texto_limpo = texto_limpo.strip()
        return texto_limpo
