from fastapi import APIRouter, UploadFile, File
from config.settings import (
    ALLOWED_EXTENSIONS,
    MAX_UPLOAD_FILES
)

router = APIRouter()

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