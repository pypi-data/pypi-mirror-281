import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DEFAULT_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api")
DB_HOST = os.getenv("OLLAMA_DB_HOST", "localhost")
DB_PORT = os.getenv("OLLAMA_DB_PORT", 27017)
DB_NAME = os.getenv("OLLAMA_DB_NAME", "ollama")
DB_USER = os.getenv("OLLAMA_DB_USER", None)
DB_PASSWORD = os.getenv("OLLAMA_DB_PASSWORD",None)
