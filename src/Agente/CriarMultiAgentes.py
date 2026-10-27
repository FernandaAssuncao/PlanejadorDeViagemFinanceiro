from uuid import uuid4
from langchain_core.tools import tool
from src.Agente.AgenteIA import AgenteIA

def criar_ferramentas_multiAgentes(ferramentas_existentes):
    """Cria agentes especialistas e os disponibiliza como ferramentas para o agente supervisor."""
    ferramentas_financeiras = {
        "calcular_orcamento_viagem",
        "converter_moeda",
        "pegar_cotacao_moeda",
        "pegar_historico_de_viagens",
        "pegar_informacoes_viagem_usuario_atualmente_planejada",
    }

    ferramentas_pesquisa = {
        "pesquisar_na_web",
        "pegar_clima_cidade",
    }

    agente_financeiro_tools = [
        ferramenta
        for ferramenta in ferramentas_existentes
        if ferramenta.name in ferramentas_financeiras
    ]

    agente_pesquisa_tools = [
        ferramenta
        for ferramenta in ferramentas_existentes
        if ferramenta.name in ferramentas_pesquisa
    ]

    agente_financeiro = AgenteIA(
        """
        Você é um agente especialista em finanças de viagens.

        Sua responsabilidade é:
        - Calcular orçamentos de viagens.
        - Consultar cotações de moedas.
        - Converter moedas.
        - Consultar o histórico financeiro de viagens.
        - Consultar os dados da viagem atualmente planejada.

        Use as ferramentas disponíveis quando necessário.
        Não invente valores nem resultados de cálculos.
        Explique os resultados com clareza.
        """
    , ferramentas=agente_financeiro_tools)

    agente_pesquisa = AgenteIA(
        """
        Você é um agente especialista em pesquisa de viagens.

        Sua responsabilidade é:
        - Pesquisar destinos, restaurantes e atrações.
        - Buscar informações atualizadas na web.
        - Consultar o clima quando necessário.

        Use as ferramentas disponíveis para buscar informações.
        Diferencie informações verificadas de sugestões.
        Não invente resultados de pesquisas.
        """
    , ferramentas=agente_pesquisa_tools)

    @tool("consultar_agente_financeiro")
    def consultar_agente_financeiro(pergunta: str) -> str:
        """Encaminha perguntas sobre orçamento, moedas,
        conversões e histórico de viagens ao agente financeiro."""

        thread_id = f"financeiro_{uuid4().hex}"

        return agente_financeiro(
            pergunta,
            thread_id=thread_id,
        )

    @tool("consultar_agente_pesquisa")
    def consultar_agente_pesquisa(pergunta: str) -> str:
        """Encaminha perguntas sobre destinos, restaurantes,
        atrações turísticas e clima ao agente de pesquisa."""

        thread_id = f"pesquisa_{uuid4().hex}"

        return agente_pesquisa(
            pergunta,
            thread_id=thread_id,
        )

    return [
        consultar_agente_financeiro,
        consultar_agente_pesquisa,
    ]
