from dotenv import load_dotenv
import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

api_key = os.getenv('API_KEY_GROQ')

# Encontra a raiz do projeto subindo duas pastas a partir do script atual (src/Agente)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Constrói o caminho exato até ao ficheiro PDF na pasta data
CAMINHO_PDF = BASE_DIR / "data" / "london-visitor-guide.pdf"

# Passa o caminho convertido para string para o teu loader (ex: PyPDFLoader)
loader = PyPDFLoader(str(CAMINHO_PDF))
