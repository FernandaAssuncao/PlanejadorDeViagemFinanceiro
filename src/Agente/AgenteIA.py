from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END

load_dotenv()
api_key = os.getenv('API_KEY_GROQ')

class AgenteIA:
    def __init__(self, system=''):
        self.system = system
        self.messages = []
        if system:
            self.messages.append({'role': 'system', 'content': self.system})
        self.modelo = ChatGroq(model='openai/gpt-oss-20b', api_key=api_key)

    def __call__(self, message):
        self.messages.append({'role': 'user', 'content': message})
        resposta = self.execute()
        self.messages.append({'role': 'assistant', 'content': resposta})
        return resposta

    def execute(self):
        prompt = ''
        for msg in self.messages:
            prompt += f'{msg["role"]}: {msg["content"]}\n'
        resposta = self.modelo.invoke(prompt)
        return resposta.content
