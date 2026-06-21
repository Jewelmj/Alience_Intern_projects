from pathlib import Path
from datetime import datetime, timedelta

from config.settings import (
    FILE_RETENTION_DAYS
)

from database.document_repository import (
    get_old_documents,
    delete_document
)

from database.vector_repository import (
    delete_document_embeddings
)

from config.logger import logger

def cleanup_old_documents():

    cutoff_date = (
        datetime.utcnow()
        - timedelta(
            days=FILE_RETENTION_DAYS
        )
    )

    old_documents = (
        get_old_documents(
            cutoff_date
        )
    )

    deleted_count = 0

    for document in old_documents:

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

        deleted_count += 1

    logger.info(
        f"Deleted {deleted_count} document(s)"
    )

    return deleted_count