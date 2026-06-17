import chromadb

from config.settings import (
    CHROMA_DB_PATH,
    CHROMA_COLLECTION
)

client = chromadb.PersistentClient(
    path=CHROMA_DB_PATH
)

collection = client.get_or_create_collection(
    name=CHROMA_COLLECTION
)