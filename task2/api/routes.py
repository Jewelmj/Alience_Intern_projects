from pathlib import Path
from fastapi import APIRouter, UploadFile, File
from io import BytesIO

from config.settings import (
    ALLOWED_EXTENSIONS,
    MAX_UPLOAD_FILES,
    UPLOAD_FOLDER,
    MAX_PDF_PAGES,
    EXTRACTED_TEXT_FOLDER
)
from config.logger import logger
from schema.utils.pdf_extraction import extract_pdf_text
from schema.utils.file_storage import get_unique_filename, save_extracted_text

router = APIRouter()

Path(UPLOAD_FOLDER).mkdir(
    parents=True,
    exist_ok=True
)
Path(EXTRACTED_TEXT_FOLDER).mkdir(
    parents=True,
    exist_ok=True
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

        text = ""
        page_count = 0
        text_filename = None
        if filename.endswith(".pdf"):

            try:
                text, page_count = extract_pdf_text(
                    BytesIO(content)
                )

                if page_count > MAX_PDF_PAGES:
                    logger.warning(
                        f"{file.filename} exceeds maximum page limit ({page_count}/{MAX_PDF_PAGES})"
                    )
                    
                    return {
                        "status": "error",
                        "message": f"{file.filename} exceeds {MAX_PDF_PAGES} pages"
                    }

                text_filename = save_extracted_text(
                    file.filename,
                    text
                )
                logger.info(
                    f"Extracted text saved: {text_filename}"
                )

            except Exception:
                logger.error(
                    f"Error occurred while processing PDF: {file.filename}"
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
                "characters": len(text),
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