from fastapi import APIRouter, UploadFile, File

router = APIRouter()


@router.get("/")
def home():
    return {"message": "API is running"}


@router.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    return {
        "files": [file.filename for file in files]
    }