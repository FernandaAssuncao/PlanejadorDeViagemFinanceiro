from dotenv import load_dotenv
import os
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from typing import TypedDict, Annotated


load_dotenv()
api_key = os.getenv('API_KEY_GROQ')


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

class AgenteIA:
    def __init__(self, system='' , ferramentas=None):
        self.system = system
        self.messages = []
        self.ferramentas = ferramentas or []
        self.modelo = ChatGroq(model='openai/gpt-oss-20b', api_key=api_key)
        self.modelo_com_ferramentas = self.modelo.bind_tools(self.ferramentas)

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

        return workflow.compile()

    def __call__(self, message):
        self.messages.append(HumanMessage(content=message))
        resposta = self.app.invoke({'messages': self.messages})
        self.messages = resposta['messages']
        print(self.messages)
        return self.messages[-1].content
