from typing import List
from fastapi import APIRouter, UploadFile, File

router = APIRouter()

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}


@router.get("/")
def home():
    return {"message": "API is running"}


@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):

    if len(files) > 3:
        return {
            "status": "error",
            "message": "Maximum 3 files allowed"
        }

    for file in files:

        filename = file.filename.lower()

        if not filename.endswith(tuple(ALLOWED_EXTENSIONS)):
            return {
                "status": "error",
                "message": f"Unsupported file type: {file.filename}"
            }

    return {
        "status": "success",
        "files": [file.filename for file in files]
    }