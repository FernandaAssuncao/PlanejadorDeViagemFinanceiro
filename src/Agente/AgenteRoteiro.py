from uuid import uuid4
from langchain_core.tools import tool
from src.Agente.AgenteIA import AgenteIA

def criar_agente_roteiro(agente_financeiro, agente_pesquisa):

    @tool("consultar_agente_financeiro")
    def consultar_financeiro(pergunta:str) -> str:
        """Consulta informações financeiras necessárias
            para elaborar um roteiro de viagem."""

        return agente_financeiro(
            pergunta,
            thread_id=f"roteiro_financeiro_{uuid4().hex}"
        )

    @tool("consultar_agente_pesquisa")
    def consultar_pesquisa(pergunta:str) -> str:
        """Pesquisa atrações turísticas, restaurantes,
        informações sobre transporte, hospedagem e outros
        detalhes relevantes para montar um roteiro de viagem."""

        return agente_pesquisa(
            pergunta,
            thread_id=f"roteiro_pesquisa_{uuid4().hex}"
        )

    ferramentas = [
        consultar_financeiro,
        consultar_pesquisa
    ]

    agente = AgenteIA(
        system="""
            Você é um agente especialista na criação de roteiros de viagem.

            Sua responsabilidade é montar roteiros organizados,
            realistas e compatíveis com as condições do usuário.

            Para elaborar um roteiro:

            1. Identifique o destino, a quantidade de dias,
               o número de viajantes e o orçamento disponível.

            2. Consulte o agente financeiro para verificar
               o orçamento e os valores necessários.

            3. Consulte o agente de pesquisa para encontrar
               atrações turísticas, restaurantes e informações
               relevantes sobre o destino.

            4. Organize as atrações em uma sequência por dia,
               considerando a localização e a duração da viagem.

            5. Evite colocar atrações demais no mesmo dia.

            6. Informe quando não houver informações suficientes
               para estimar algum custo.

            7. Nunca invente preços, horários ou disponibilidade.

            FORMATO DA RESPOSTA:

            - Destino
            - Duração
            - Orçamento
            - Roteiro do dia 1 até o último dia
            - Atrações sugeridas
            - Estimativas de gastos, quando disponíveis
            - Observações importantes

            Não confunda estimativas com valores confirmados.
            """,
        ferramentas=ferramentas
    )

    return agente
