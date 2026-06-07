from typing import List
from fastapi import APIRouter, UploadFile, File
from pathlib import Path
from pypdf import PdfReader
from io import BytesIO
from config.settings import (
    ALLOWED_EXTENSIONS,
    MAX_FILES,
    MAX_PDF_PAGES
)

router = APIRouter()

UPLOAD_DIR = Path("storage/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.get("/")
def home():
    return {"message": "API is running"}


@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):

    if len(files) > MAX_FILES:
        return {
            "status": "error",
            "message": "Maximum 3 files allowed"
        }

    for file in files:

        filename = file.filename.lower()

        # Check file extension
        if not filename.endswith(tuple(ALLOWED_EXTENSIONS)):
            return {
                "status": "error",
                "message": f"Unsupported file type: {file.filename}"
            }

        # Read file contents
        content = await file.read()

        # PDF page validation
        if filename.endswith(".pdf"):

            pdf_reader = PdfReader(BytesIO(content))
            page_count = len(pdf_reader.pages)

            if page_count > MAX_PDF_PAGES:
                return {
                    "status": "error",
                    "message": f"{file.filename} exceeds {MAX_PDF_PAGES} pages"
                }

        # Save file
        file_path = UPLOAD_DIR / file.filename

        with open(file_path, "wb") as buffer:
            buffer.write(content)

    return {
    "status": "success",
    "message": "Files uploaded successfully",
    "files": [file.filename for file in files]
}