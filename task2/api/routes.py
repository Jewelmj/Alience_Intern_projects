from fastapi import APIRouter, UploadFile, File

router = APIRouter()

@router.post("/single")
async def single_file(file: UploadFile = File(...)):
    return {"name": file.filename}