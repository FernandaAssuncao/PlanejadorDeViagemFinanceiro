from dotenv import load_dotenv
import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

api_key = os.getenv('API_KEY_GROQ')

model = ChatGroq(model='openai/gpt-oss-20b', api_key=api_key)

# Encontra a raiz do projeto subindo duas pastas a partir do script atual (src/Agente)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Constrói o caminho exato até ao ficheiro PDF na pasta data
CAMINHO_PDF = BASE_DIR / "data" / "london-visitor-guide.pdf"

# Passa o caminho convertido para string para o teu loader (ex: PyPDFLoader)
loader = PyPDFLoader(str(CAMINHO_PDF)).load()

embeddings = HuggingFaceEmbeddings(
    model="intfloat/multilingual-e5-base"
)

pedacos = SemanticChunker(embeddings=embeddings,
                          breakpoint_threshold_type='percentile').split_documents(loader)

vectorstore = FAISS.from_documents(pedacos, embeddings).as_retriever(search_kwargs={"k": 2})

prompt_template = ChatPromptTemplate.from_messages([
    ('system', 'Você é um especialista em viagens, seu trabalho é receber o contexto(a maior parte deles em ingles) e utilizar para formular uma resposta adequada ao usuario'),
    ('human', '{query}\nContexto: {context}\nResposta: ')
])

cadeia = prompt_template | model | StrOutputParser()

def responder(pergunta: str):
    trecos = vectorstore.invoke(pergunta)
    contexto = '\n\n'.join(um_treco.page_content for um_treco in trecos)
    return cadeia.invoke({
        'query': pergunta,
        'context': contexto
    })
print(responder('Me fale informações interessantes sobre londres, quais os melhores lugares para visitar?'))