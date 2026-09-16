from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

load_dotenv()
api_key = os.getenv('API_KEY_GROQ')

class AgenteIA:
    def __init__(self, system='' , ferramentas=None):
        self.system = system
        self.messages = []
        self.ferramentas = ferramentas or []
        if system:
            self.messages.append({'role': 'system', 'content': self.system})
        self.modelo = ChatGroq(model='openai/gpt-oss-20b', api_key=api_key)
        if self.ferramentas:
            self.modelo_com_ferramentas = self.modelo.bind_tools(self.ferramentas)

    def __call__(self, message):
        self.messages.append({'role': 'user', 'content': message})
        resposta = self.execute()
        self.messages.append({'role': 'assistant', 'content': resposta})
        return resposta

    def execute(self):
        prompt = ''
        for msg in self.messages:
            prompt += f'{msg["role"]}: {msg["content"]}\n'
        response = self.modelo_com_ferramentas.invoke(prompt)
        ferramentas_mapeadas = {ferramenta.name: ferramenta for ferramenta in self.ferramentas}
        if response.tool_calls:
            message_turno = [response]
            for acao in response.tool_calls:
                print('O modelo decidiu usar uma Ferramenta.')
                nome_funcao = acao["name"]
                print(f'Nome função: {nome_funcao}')
                argurmentos = acao["args"]

                if nome_funcao in ferramentas_mapeadas:
                    resultado_ferramenta = ferramentas_mapeadas[nome_funcao].invoke(argurmentos)
                    from langchain_core.messages import ToolMessage
                    message_turno.append(
                        ToolMessage(content=str(resultado_ferramenta), tool_call_id=acao['id'])
                    )

                    resposta_final_modelo = self.modelo_com_ferramentas.invoke(
                        self.messages + message_turno
                    )
                    return resposta_final_modelo.content

        return response.content
