from dotenv import load_dotenv
import os
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from typing import TypedDict, Annotated
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import trim_messages
import sqlite3


load_dotenv()
api_key = os.getenv('API_KEY_GROQ')


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

class AgenteIA:
    def __init__(self, system='' , ferramentas=None):
        self.system = system
        self.ferramentas = ferramentas or []
        self.modelo = ChatGroq(model='openai/gpt-oss-120b', api_key=api_key)
        self.modelo_com_ferramentas = self.modelo.bind_tools(self.ferramentas)

        self.conn = sqlite3.connect('./data/agente.db', check_same_thread=False)

        self.checkpointer = SqliteSaver(self.conn)

        self.checkpointer.setup()

        self.app = self.criar_grafo()

    def criar_grafo(self):
        """Método interno que monta o fluxo do LangGraph para a classe."""
        workflow = StateGraph(AgentState)

        def chamar_modelo(state: AgentState):
            mensagens_recentes = trim_messages(
                state["messages"],
                max_tokens=4500,
                token_counter=self.modelo,
                strategy="last",
                include_system=True,
                allow_partial=False
            )

            response = self.modelo_com_ferramentas.invoke(mensagens_recentes)

            return {"messages": [response]}

        workflow.add_node("chatbot", chamar_modelo)

        workflow.add_node(
            "tools",
            ToolNode(self.ferramentas)
        )

        workflow.set_entry_point("chatbot")

        workflow.add_conditional_edges(
            "chatbot",
            lambda state:
            "tools"
            if state["messages"][-1].tool_calls
            else END
        )

        workflow.add_edge(
            "tools",
            "chatbot")

        return workflow.compile(checkpointer=self.checkpointer)

    def __call__(self, message, thread_id:str = 'thread_padrao'):
        config = {'configurable': {'thread_id': thread_id}}

        estado = self.app.get_state(config)

        mensagens = []

        # Adiciona o prompt de sistema somente no início da conversa
        if not estado.values.get('messages'):
            mensagens.append(SystemMessage(content=self.system))

        mensagens.append(HumanMessage(content=message))
        resposta = self.app.invoke({'messages': mensagens}, config=config)

        return resposta['messages'][-1].content
