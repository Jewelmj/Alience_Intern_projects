from pathlib import Path
from fastapi import APIRouter, UploadFile, File

from config.settings import (
    ALLOWED_EXTENSIONS,
    MAX_UPLOAD_FILES,
    UPLOAD_FOLDER,
    MAX_PDF_PAGES,
    EXTRACTED_TEXT_FOLDER
)
from config.logger import logger
from schema.utils.file_storage import get_unique_filename
from agents.extraction.agent import (
    ExtractionAgent
)

router = APIRouter()

Path(UPLOAD_FOLDER).mkdir(
    parents=True,
    exist_ok=True
)
Path(EXTRACTED_TEXT_FOLDER).mkdir(
    parents=True,
    exist_ok=True
)

extraction_agent = ExtractionAgent()


@router.get("/")
def home():
    return {"message": "API is running"}


@router.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    logger.info(
        f"Upload request received with {len(files)} file(s)"
    )

    if len(files) > MAX_UPLOAD_FILES:
        logger.warning(
            f"Upload rejected: received {len(files)} files, maximum allowed is {MAX_UPLOAD_FILES}"
        )

        return {
            "status": "error",
            "message": f"Maximum {MAX_UPLOAD_FILES} files allowed"
        }

    saved_files = []

    for file in files:

        filename = file.filename.lower()

        if not filename.endswith(tuple(ALLOWED_EXTENSIONS)):
            logger.warning(
                f"Unsupported file type: {file.filename}"
            )

            return {
                "status": "error",
                "message": f"Unsupported file type: {file.filename}"
            }
        
        content = await file.read()

        page_count = 0
        text_filename = None
        characters = 0
        if filename.endswith(".pdf"):

            try:
                metadata = extraction_agent.process(
                    file.filename,
                    content,
                    MAX_PDF_PAGES
                )

                page_count = metadata["page_count"]

                text_filename = metadata["text_file"]

                characters = metadata["characters"]

                logger.info(
                    f"Extracted text saved: {text_filename}"
                )

            except ValueError as e:

                logger.warning(str(e))

                return {
                    "status": "error",
                    "message": str(e)
                }

            except Exception as e:

                logger.error(
                    f"Error occurred while processing PDF {file.filename}: {e}"
                )

                return {
                    "status": "error",
                    "message": f"Unable to read PDF: {file.filename}"
                }
            
        file_path = Path(UPLOAD_FOLDER) / file.filename

        file_path = get_unique_filename(file_path)

        with open(file_path, "wb") as buffer:
            buffer.write(content)

        logger.info(
            f"File saved successfully: {file_path.name}"
        )

        saved_files.append(
            {
                "filename": file_path.name,
                "page_count": page_count,
                "characters": characters,
                "text_file": text_filename
            }
        )
    
    logger.info(
        f"Upload completed successfully. Saved {len(saved_files)} file(s)"
    )

    return {
        "status": "success",
        "files": saved_files
    }