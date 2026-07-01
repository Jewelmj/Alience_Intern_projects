from pathlib import Path
from datetime import UTC, datetime

from config.settings import (
    ALLOWED_EXTENSIONS,
    MAX_PDF_PAGES,
    UPLOAD_FOLDER,
    ENABLE_EPHEMERAL_STORAGE
)

from schema.utils.session_cleanup import (
    cleanup_expired_sessions
)

from schema.utils.text_chunking import (
    chunk_text
)

from database.vector_repository import (
    save_embeddings
)

from schema.utils.file_storage import (
    get_unique_filename,
)

from schema.utils.file_validation import (
    is_allowed_extension
)

from config.logger import logger

from database.document_repository import (
    create_document
)

from schema.exceptions.ingestion import (
    EmptyDocumentError
)


class IngestionAgent:

    def __init__(self, extraction_agent, embedding_agent):
        self.extraction_agent = extraction_agent
        self.embedding_agent = embedding_agent

    def process_file(self,file,content,session_id):
        filename = file.filename.lower()

        if not is_allowed_extension(
            filename,
            ALLOWED_EXTENSIONS
        ):
            raise ValueError(
                f"Unsupported file type: {file.filename}"
            )

        metadata = {
            "page_count": 0,
            "characters": 0,
            "text_file": None
        }

        if filename.endswith(
            (".pdf", ".png", ".jpg", ".jpeg", ".txt")
        ):
            metadata = self.extraction_agent.process(
                file.filename,
                content,
                MAX_PDF_PAGES
            )

        text = metadata["text"]

        if not text.strip():
            logger.warning(
                f"No text extracted from {file.filename}"
            )

            raise EmptyDocumentError(
                f"No extractable text found in {file.filename}"
            )

        chunks = chunk_text(text)

        file_path = (
            Path(UPLOAD_FOLDER)
            / file.filename
        )

        file_path = get_unique_filename(
            file_path
        )

        file_path.write_bytes(content)

        logger.info(
            f"File saved successfully: {file_path.name}"
        )

        metadata.pop("text", None)

        document = {
            "filename": file_path.name,
            "uploaded_at": datetime.now(UTC),
            "last_accessed": datetime.now(UTC),
            **metadata,
            "chunk_count": len(chunks),
        }

        document_id = create_document(
            document
        )

        logger.info(
            f"Document metadata stored in MongoDB: {document_id}"
        )

        chunk_metadata = []

        for idx, chunk in enumerate(chunks):

            chunk_metadata.append(
                {
                    "document_id": document_id,
                    "chunk_id": idx,
                    "session_id": session_id,
                    "source_file": file_path.name,
                    "chunk_length": len(chunk),
                    "text": chunk
                }
            )

        logger.info(
            f"Chunk metadata processed. Total chunks: {len(chunk_metadata)}"
        )

        embedding_records = (
            self.embedding_agent.generate_embeddings(
                chunk_metadata
            )
        )


        save_embeddings(
            embedding_records
        )

        if ENABLE_EPHEMERAL_STORAGE:

            deleted_count = (
                cleanup_expired_sessions()
            )

            logger.info(
                "Ephemeral storage cleanup completed. "
                f"{deleted_count} expired session(s) removed."
            )

        return {
            "document_id": document_id,
            "filename": file_path.name,
            **metadata
        }