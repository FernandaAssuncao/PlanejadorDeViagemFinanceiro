import customtkinter as ctk
from .Agente.AgenteIA import AgenteIA
from .APIS.Cotacao import Cotacao
from .APIS.Clima import ClimaService
from .GerenciadorDeDados.GerenciadorDeDados import GerenciadorDeDados
from langchain_core.tools import tool
from langchain_core.messages import AIMessage, ToolMessage
from .Agente.CriarMultiAgentes import criar_ferramentas_multiAgentes
from dotenv import load_dotenv
from tavily import TavilyClient
import threading
import re
import json
import os

load_dotenv()

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
            elif moeda == 'bitcoin':
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

        @tool("pegar_historico_de_viagens")
        def pegar_historico_de_viagens() -> list:
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

        @tool
        def calcular_orcamento_viagem(orcamento:float, viajantes:int, dias: int) -> dict:
            """Retorna os resultados dos calculos da viagem, como orçamento por dia,
            orçamento por dia/pessoa e orçamento por viajantes. O usuario precisa informar o
            orçamento,  o numero de viajantes e a quantidade de dias."""
            try:
                por_dia = orcamento / dias
                por_pessoa = orcamento / viajantes
                por_pessoa_dia = orcamento / viajantes / dias
                return {'Orçamento por dia': por_dia,
                        'Orçamento por pessoa': por_pessoa,
                        'Orçamento por dia/pessoa': por_pessoa_dia}
            except (ZeroDivisionError, ValueError):
                return {'Erro': 'Alguma informação ou calculo deu errado.'}

        @tool
        def converter_moeda(valor:float, cotacao:float) -> str:
            """Retorna o valor pedido para a moeda solicitada.
            Ex: o usuario quer saber quanto é R$560 em euro.
            ESSA FUNÇÃO CONVERTE APENAS VALORES EM REAIS PARA A MOEDA SOLICITADA.
            Execute a ferramenta pegar_cotacao_moeda para saber a cotação se ainda não sabe.
            """
            c = Cotacao()
            resultado = c.calcular_valor_para_a_moeda_ia(valor, cotacao)
            return f'R$ {valor:.2f} = {resultado:.2f}'

        @tool
        def pesquisar_na_web(consulta: str) -> str:
            """
            Pesquisa informações atuais na Web sobre destinos,
            atrações turísticas, transporte, hospedagem e custos
            de viagem. Use quando a resposta depender de informações
            externas ou atualizadas.
            A consulta deve descrever claramente o que precisa ser buscado."""
            api_key = os.getenv('TAVILY_API_KEY')
            if not api_key:
                return "Erro: a chave da API Tavily não foi configurada."
            try:
                cliente = TavilyClient(api_key=api_key)

                resultado = cliente.search(
                    query=consulta,
                    search_depth='basic',
                    max_results=5
                )

                resultados = resultado.get("results", [])

                if not resultados:
                    return 'Nenhum resultado encontrado.'

                fontes = []

                for item in resultados:
                    fontes.append({
                        "titulo": item.get("title", ""),
                        "url": item.get("url", ""),
                        "conteudo": item.get("content", "")[:1200]
                    })

                return json.dumps(
                    fontes,
                    ensure_ascii=False,
                    indent=2
                )
            except Exception as erro:
                return (
                    "Não foi possível realizar a pesquisa na Web. "
                    f"Erro: {type(erro).__name__}"
                )

        self.ferramentas = [pegar_informacoes_viagem_usuario_atualmente_planejada,
                            pegar_cotacao_moeda,
                            pegar_clima_cidade,
                            pegar_historico_de_viagens,
                            calcular_orcamento_viagem,
                            converter_moeda,
                            pesquisar_na_web]

        ferramentas_agente = criar_ferramentas_multiAgentes(self.ferramentas)

        self.assistente = AgenteIA('''
              Você é o supervisor de um sistema inteligente de planejamento de viagens.
            Você possui dois agentes especialistas:
            1. consultar_agente_financeiro:
               Responsável por orçamento, cotação de moedas, conversões,
               viagem atualmente planejada e histórico de viagens.
            2. consultar_agente_pesquisa:
               Responsável por pesquisar destinos, restaurantes,
               atrações turísticas e consultar o clima.
            REGRAS OBRIGATÓRIAS DE ROTEAMENTO:
            - Se o usuário perguntar quantas viagens existem no histórico,
              quais viagens já planejou, quais destinos visitou ou planejou
              anteriormente, ou pedir uma comparação entre viagens passadas,
              chame consultar_agente_financeiro.
            - Se o usuário perguntar sobre o orçamento da viagem atual,
              cotações, conversões de moedas ou dados da viagem planejada,
              chame consultar_agente_financeiro.
            - Se o usuário perguntar sobre restaurantes, atrações turísticas,
              destinos ou pesquisas na web, chame consultar_agente_pesquisa.
            - Se perguntar sobre o clima, chame consultar_agente_pesquisa.
            - Nunca responda que não tem acesso ao histórico sem antes
              consultar o agente financeiro.
            - Depois de receber o resultado do especialista, responda
              diretamente ao usuário, sem inventar informações.''',
                                   ferramentas=ferramentas_agente)

        #self.testar_agente()
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
            resposta_ia_texte = self.assistente(texto, thread_id='teste_multiagentes_002')

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

    def testar_agente(self):
        config = {
            "configurable": {
                "thread_id": "nova_conversa"
            }
        }
        agente = self.assistente
        estado = agente.app.get_state(config)
        mensagens = estado.values.get("messages", [])

        print("\n===== DIAGNÓSTICO DO AGENTE =====")
        print("Thread ID:", config["configurable"]["thread_id"])
        print("Total de mensagens:", len(mensagens))
        print("Estado encontrado:", bool(estado.values))

        ids_chamadas = set()
        ids_respostas = set()

        for i, mensagem in enumerate(mensagens):
            print(f"\nMensagem {i}")
            print("Tipo:", type(mensagem).__name__)
            print("Conteúdo:", str(mensagem.content)[:200])

            if isinstance(mensagem, AIMessage):
                chamadas = getattr(mensagem, "tool_calls", []) or []

                for chamada in chamadas:
                    nome = chamada.get("name")
                    chamada_id = chamada.get("id")

                    print("Nome da ferramenta:", nome)
                    print("ID da chamada:", chamada_id)
                    print("Argumentos:", chamada.get("args"))

                    if not nome:
                        print("ALERTA: chamada sem nome!")

                    if chamada_id:
                        ids_chamadas.add(chamada_id)

            elif isinstance(mensagem, ToolMessage):
                chamada_id = getattr(
                    mensagem, "tool_call_id", None
                )

                print("Nome:", getattr(mensagem, "name", None))
                print("Tool call ID:", chamada_id)

                if chamada_id:
                    ids_respostas.add(chamada_id)

        print("\n===== VERIFICAÇÃO FINAL =====")

        sem_resposta = ids_chamadas - ids_respostas
        sem_chamada = ids_respostas - ids_chamadas

        print("Chamadas sem resposta:", sem_resposta)
        print("Respostas sem chamada:", sem_chamada)

        print("===== FIM DO DIAGNÓSTICO =====")