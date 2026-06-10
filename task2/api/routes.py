from pathlib import Path
from fastapi import APIRouter, UploadFile, File
from io import BytesIO
from pypdf import PdfReader

from config.settings import (
    ALLOWED_EXTENSIONS,
    MAX_UPLOAD_FILES,
    UPLOAD_FOLDER,
    MAX_PDF_PAGES
)
from config.logger import logger

router = APIRouter()

Path(UPLOAD_FOLDER).mkdir(
    parents=True,
    exist_ok=True
)

def get_unique_filename(file_path: Path) -> Path:
    """
    Prevent overwriting existing files.
    Example:
        report.pdf
        report_1.pdf
        report_2.pdf
    """

    if not file_path.exists():
        return file_path

    stem = file_path.stem
    suffix = file_path.suffix

    counter = 1

    while True:

        new_path = (
            file_path.parent
            / f"{stem}_{counter}{suffix}"
        )

        if not new_path.exists():
            return new_path

        counter += 1

@router.get("/")
def home():
    return {"message": "API is running"}


@router.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):

    if len(files) > MAX_UPLOAD_FILES:
        return {
            "status": "error",
            "message": f"Maximum {MAX_UPLOAD_FILES} files allowed"
        }

    saved_files = []

    for file in files:

        filename = file.filename.lower()

        if not filename.endswith(tuple(ALLOWED_EXTENSIONS)):
            return {
                "status": "error",
                "message": f"Unsupported file type: {file.filename}"
            }
        
        content = await file.read()

        if filename.endswith(".pdf"):

            try:
                pdf_reader = PdfReader(BytesIO(content))
                page_count = len(pdf_reader.pages)

                if page_count > MAX_PDF_PAGES:
                    return {
                        "status": "error",
                        "message": f"{file.filename} exceeds {MAX_PDF_PAGES} pages"
                    }

            except Exception:
                return {
                    "status": "error",
                    "message": f"Unable to read PDF: {file.filename}"
                }
            
        file_path = Path(UPLOAD_FOLDER) / file.filename

        file_path = get_unique_filename(file_path)

        with open(file_path, "wb") as buffer:
            buffer.write(
                await file.read()
            )

        saved_files.append(
            file_path.name
        )

    return {
        "status": "success",
        "files": saved_files
    }