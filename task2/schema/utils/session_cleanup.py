from pathlib import Path
from datetime import datetime, timedelta, UTC

from config.settings import (
    FILE_RETENTION_DAYS,
    SESSION_TIMEOUT_MINUTES
)

from database.document_repository import (
    get_old_documents,
    delete_document,
    get_expired_sessions
)

from database.vector_repository import (
    delete_document_embeddings
)

from config.logger import logger

def delete_document_resources(document):
    filename = document["filename"]

    delete_document_embeddings(
        filename
    )

    files_to_delete = [

        Path("storage/uploads")
        / filename,

        Path(
            "storage/extracted_text"
        )
        / document.get(
            "text_file",
            ""
        ),

        Path(
            "storage/chunks"
        )
        / document.get(
            "chunk_metadata_file",
            ""
        ),

        Path(
            "storage/vectors"
        )
        / document.get(
            "vector_file",
            ""
        )
    ]

    for file_path in files_to_delete:

        if file_path.name == ".gitkeep":
            continue

        if file_path.exists():

            file_path.unlink()

            logger.info(
                f"Deleted {file_path}"
            )

    delete_document(
        str(document["_id"])
    )

def cleanup_expired_sessions():
    cutoff = (
        datetime.now(UTC)
        - timedelta(
            minutes=SESSION_TIMEOUT_MINUTES
        )
    )

    expired_documents = (
        get_expired_sessions(
            cutoff
        )
    )

    deleted = 0

    for document in expired_documents:

        delete_document_resources(
            document
        )

        deleted += 1

    return deleted
