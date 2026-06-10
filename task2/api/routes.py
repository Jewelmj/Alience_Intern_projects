from pathlib import Path
from fastapi import APIRouter, UploadFile, File

from config.settings import (
    MAX_UPLOAD_FILES,
    UPLOAD_FOLDER,
    EXTRACTED_TEXT_FOLDER
)
from config.logger import logger
from agents.ingestion.agent import (
    IngestionAgent
)
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
ingestion_agent = IngestionAgent(
    extraction_agent
)


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

        content = await file.read()

        try:
            result = ingestion_agent.process_file(file, content)
            saved_files.append(result)

        except ValueError as e:
            logger.warning(str(e))

            return {
                "status": "error",
                "message": str(e)
            }

        except Exception as e:
            logger.error(
                f"Failed to process {file.filename}: {e}"
            )

            return {
                "status": "error",
                "message": f"Unable to process file: {file.filename}"
            }
    
    logger.info(
        f"Upload completed successfully. Saved {len(saved_files)} file(s)"
    )

    return {
        "status": "success",
        "files": saved_files
    }