from dotenv import load_dotenv
import os
from openai import OpenAI

# Ruta relativa al directorio del script (openai_client.py)
env_path = Path(__file__).resolve().parent.parent.parent / ".env"  # Ajusta según tu estructura
load_dotenv(dotenv_path=env_path)

# Configuración inicial
API_KEY = os.getenv("API_KEY_IA")
ASSISTANT_ID = os.getenv('ASSISTANT_ID_IA')
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"txt", "pdf", "docx", "doc", "xls", "xlsx"}

# Inicializa el cliente de OpenAI
client = OpenAI(api_key=API_KEY)

# Diccionario para almacenar el historial de conversaciones por usuario
user_conversations = {}