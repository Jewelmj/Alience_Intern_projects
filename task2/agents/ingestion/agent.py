from pathlib import Path

from config.settings import (
    ALLOWED_EXTENSIONS,
    MAX_PDF_PAGES,
    UPLOAD_FOLDER
)
from schema.utils.text_chunking import (
    chunk_text
)

from schema.utils.chunk_storage import (
    save_chunk_metadata
)
from schema.utils.vector_storage import (
    save_vectors
)
from schema.utils.file_storage import (get_unique_filename,)
from schema.utils.file_validation import (is_allowed_extension)
from config.logger import logger
from database.document_repository import (
    create_document
)


class IngestionAgent:

    def __init__(self, extraction_agent, embedding_agent):
        self.extraction_agent = extraction_agent
        self.embedding_agent = embedding_agent

    def process_file(self,file,content):

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

        chunks = chunk_text(
            metadata["text"]
        )

        chunk_metadata, chunk_metadata_file = (
            save_chunk_metadata(
                file.filename,
                chunks
            )
        )

        logger.info(
            f"Chunk metadata saved: {chunk_metadata_file}"
        )
        
        metadata.pop("text", None)

        embedding_records = (
            self.embedding_agent.generate_embeddings(
                chunk_metadata
            )
        )

        vector_file = save_vectors(
            file.filename,
            embedding_records
        )

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
        

        document = {
            "filename": file_path.name,
            **metadata,
            "chunk_count": len(chunks),
            "vector_file": vector_file
        }
        document_id = create_document(document)

        logger.info(
            "Skipping MongoDB storage"
        )

        return {
            "document_id": document_id,
            "filename": file_path.name,
            **metadata
        }