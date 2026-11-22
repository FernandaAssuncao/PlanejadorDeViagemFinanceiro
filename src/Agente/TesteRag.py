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

prompt_busca = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a semantic search specialist. Convert the user's Portuguese question "
        "into a concise, effective search query in English for a travel vector database. "
        "Return ONLY the search query, with no quotes, labels, or explanations."
    ),
    ("human", "{query}")
])

prompt_template = ChatPromptTemplate.from_messages([
    (
        "system",
        "Você é um especialista em viagens. Responda em português usando EXCLUSIVAMENTE "
        "as informações fornecidas no contexto (que pode estar em inglês). "
        "Não invente informações e não use conhecimento externo. "
        "Se a resposta não estiver no contexto, diga claramente que não encontrou essa informação no material."
    ),
    ("human", "Pergunta: {query}\n\nContexto:\n{context}\n\nResposta:")
])

cadeia_busca = prompt_busca | model | StrOutputParser()
cadeia = prompt_template | model | StrOutputParser()

retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

def responder(pergunta: str, debug: bool = False) -> str:
    busca = cadeia_busca.invoke({"query": pergunta}).strip()
    documentos_relevantes = retriever.invoke(f"query: {busca}")

    if debug:
        print("Query gerada:", busca)
        print("Qtd. chunks recuperados:", len(documentos_relevantes))

    contexto = "\n\n---\n\n".join(
        doc.page_content.removeprefix("passage: ")
        for doc in documentos_relevantes
    )

    return cadeia.invoke({
        "query": pergunta,
        "context": contexto
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
print(responder('Quais são todas as opções de transporte público disponíveis em Londres?', debug=True))
