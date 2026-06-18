from pathlib import Path

from config.settings import (
    LOG_FOLDER,
    UPLOAD_FOLDER,
    EXTRACTED_TEXT_FOLDER,
    LOG_FOLDER,
)

def initialize_storage():

    folders = [
        LOG_FOLDER,
        UPLOAD_FOLDER,
        EXTRACTED_TEXT_FOLDER,
        "storage/chunks",
        "storage/vectors",
        "storage/chromadb"
    ]

    for folder in folders:

        Path(folder).mkdir(
            parents=True,
            exist_ok=True
        )