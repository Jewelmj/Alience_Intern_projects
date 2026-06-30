import os

from dotenv import load_dotenv

load_dotenv()

ALLOWED_EXTENSIONS = set(
    os.getenv(
        "ALLOWED_EXTENSIONS",
        ".pdf,.png,.jpg,.jpeg"
    ).split(",")
)

MAX_UPLOAD_FILES = int(
    os.getenv(
        "MAX_UPLOAD_FILES",
        3
    )
)

MAX_PDF_PAGES = int(
    os.getenv(
        "MAX_PDF_PAGES",
        5
    )
)

UPLOAD_FOLDER = os.getenv(
    "UPLOAD_FOLDER",
    "storage/uploads"
)

LOG_FOLDER = os.getenv(
    "LOG_FOLDER",
    "logs"
)

LOG_FILE = os.getenv(
    "LOG_FILE",
    "app.log"
)

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)

EXTRACTED_TEXT_FOLDER = os.getenv(
    "EXTRACTED_TEXT_FOLDER",
    "storage/extracted_text"
)

CHUNK_SIZE = int(
    os.getenv(
        "CHUNK_SIZE",
        500
    )
)

CHUNK_OVERLAP = int(
    os.getenv(
        "CHUNK_OVERLAP",
        100
    )
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "all-MiniLM-L6-v2"
)

MONGO_URI = os.getenv(
    "MONGO_URI"
)

MONGO_DB_NAME = os.getenv(
    "MONGO_DB_NAME"
)

CHROMA_DB_PATH = os.getenv(
    "CHROMA_DB_PATH",
    "storage/chromadb"
)

CHROMA_COLLECTION = os.getenv(
    "CHROMA_COLLECTION",
    "documents"
)

RETRIEVAL_TOP_K = int(
    os.getenv(
        "RETRIEVAL_TOP_K",
        5
    )
)

RELEVANCE_MAX_DISTANCE = float(
    os.getenv(
        "RELEVANCE_MAX_DISTANCE",
        1.5
    )
)

LLM_PROVIDER = os.getenv(
    "LLM_PROVIDER",
    "ollama"
)

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2"
)

OLLAMA_TIMEOUT = int(
    os.getenv(
        "OLLAMA_TIMEOUT",
        120
    )
)

OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)

OPENROUTER_MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "openai/gpt-4.1-mini"
)

OPENROUTER_BASE_URL = os.getenv(
    "OPENROUTER_BASE_URL",
    "https://openrouter.ai/api/v1"
)

NOT_FOUND_MESSAGE = os.getenv(
    "NOT_FOUND_MESSAGE",
    "I could not find information about that in the uploaded documents."
)

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000"
)

FILE_RETENTION_DAYS = int(
    os.getenv(
        "FILE_RETENTION_DAYS",
        30
    )
)