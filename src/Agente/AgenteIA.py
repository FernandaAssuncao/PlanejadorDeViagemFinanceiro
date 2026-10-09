from dotenv import load_dotenv
import os
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from typing import TypedDict, Annotated
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3


load_dotenv()
api_key = os.getenv('API_KEY_GROQ')


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

class AgenteIA:
    def __init__(self, system='' , ferramentas=None):
        self.system = system
        self.messages = []
        self.ferramentas = ferramentas or []
        self.modelo = ChatGroq(model='openai/gpt-oss-120b', api_key=api_key)
        self.modelo_com_ferramentas = self.modelo.bind_tools(self.ferramentas)

        self.conn = sqlite3.connect('./data/agente.db', check_same_thread=False)

        self.checkpointer = SqliteSaver(self.conn)

        self.checkpointer.setup()

        if system:
            if self.system:
                self.messages.append(
                    SystemMessage(content=self.system)
                )
        self.app = self.criar_grafo()

    def criar_grafo(self):
        """Método interno que monta o fluxo do LangGraph para a classe."""
        workflow = StateGraph(AgentState)

        def chamar_modelo(state: AgentState):
            response = self.modelo_com_ferramentas.invoke(state["messages"])

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
        self.messages.append(HumanMessage(content=message))
        resposta = self.app.invoke({'messages': self.messages}, config=config)
        self.messages = resposta['messages']
        return self.messages[-1].content
