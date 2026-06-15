from pathlib import Path

from config.settings import (
    ALLOWED_EXTENSIONS,
    MAX_PDF_PAGES,
    UPLOAD_FOLDER
)

from schema.utils.file_storage import (get_unique_filename,)
from schema.utils.file_validation import (is_allowed_extension)
from config.logger import logger
from database.document_repository import (
    create_document
)


class IngestionAgent:

    def __init__(self,extraction_agent):
        self.extraction_agent = extraction_agent

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
            **metadata
        }
        document_id = create_document(document)

        logger.info(
            f"Document metadata stored: {document_id}"
        )

        return {
            "document_id": document_id,
            "filename": file_path.name,
            **metadata
        }