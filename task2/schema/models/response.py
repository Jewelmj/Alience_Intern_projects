from pydantic import BaseModel


class FileResponse(BaseModel):

    document_id: str
    filename: str
    page_count: int | None
    characters: int
    text_file: str | None


class UploadResponse(BaseModel):

    status: str
    files: list[FileResponse]

class ErrorResponse(BaseModel):

    status: str
    message: str