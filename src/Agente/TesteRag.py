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
from langchain_core.documents import Document

load_dotenv()

api_key = os.getenv('API_KEY_GROQ')

model = ChatGroq(model='openai/gpt-oss-20b', api_key=api_key)

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"

documentos = []

arquivos_pdf = sorted(DATA_DIR.glob('*.pdf'))

if not arquivos_pdf:
    raise FileNotFoundError("Nenhum PDF encontrado na pasta data.")

for arquivo in arquivos_pdf:
    loader = PyPDFLoader(str(arquivo))
    documentos.extend(loader.load())

embeddings = HuggingFaceEmbeddings(
    model="intfloat/multilingual-e5-base",
    encode_kwargs={"normalize_embeddings": True}
)

splitter = SemanticChunker(embeddings=embeddings,
                          breakpoint_threshold_type='percentile')

pedacos = splitter.split_documents(documentos)

pedacos = [
    Document(
        page_content=f"passage: {doc.page_content}",
        metadata=doc.metadata
    )
    for doc in pedacos
]

print("Total de chunks:", len(pedacos))

for i, doc in enumerate(pedacos):
    if "museum" in doc.page_content.lower():
        print(f"\nCHUNK {i}")
        print("Tamanho:", len(doc.page_content))
        print("Página:", doc.metadata.get("page"))
        print(doc.page_content[:1000])

vectorstore = FAISS.from_documents(pedacos, embeddings)

retriver = vectorstore.as_retriever(search_kwargs={"k": 3})

prompt_template = ChatPromptTemplate.from_messages([
    ('system', 'Você é um especialista em viagens, seu trabalho é receber o contexto(a maior parte deles em ingles) e utilizar para formular uma resposta adequada ao usuario. Se o contexto não contiver a resposta, diga que não encontrou essa informação nos documentos.'),
    ('human', '{query}\nContexto: {context}\nResposta: ')
])

prompt_busca = ChatPromptTemplate.from_messages([
    ('system', 'You are an expert in semantic search; your task is to take a question and transform it into a search query for a vector database. Note: (You will always receive the question in Portuguese).'),
    ('human', '{query}')
])

cadeia = prompt_template | model | StrOutputParser()

cadeia_busca = prompt_busca | model | StrOutputParser()

def responder(pergunta: str):
    busca = cadeia_busca.invoke({'query': pergunta})
    trecos = retriver.invoke(f'query: {busca}')
    contexto = '\n\n'.join(
        trecho.page_content.removeprefix("passage: ")
        for trecho in trecos)

    return cadeia.invoke({
        'query': pergunta,
        'context': contexto
    })

def testar_busca(pergunta: str):
    resultados = vectorstore.similarity_search_with_score(
        f"query: {pergunta}",
        k=10
    )

    for i, (doc, distancia) in enumerate(resultados, start=1):
        print(f"\n========== CHUNK {i} ==========")
        print("Distância:", distancia)
        print("Fonte:", doc.metadata.get("source"))
        print("Página:", doc.metadata.get("page"))
        print("Conteúdo:", doc.page_content[:1000])

#testar_busca('Quais museus eu posso visitar em londres.')
print(responder('Quais museus eu posso visitar em Londres?'))
