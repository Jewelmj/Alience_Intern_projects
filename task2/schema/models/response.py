from pydantic import BaseModel

class HomeResponse(BaseModel):
    message: str

class FileResponse(BaseModel):

    document_id: str
    filename: str
    page_count: int | None
    characters: int
    text_file: str | None


class UploadResponse(BaseModel):

    status: str
    files: list[FileResponse]
    session_id: str
    warnings: list[str] = []

class ErrorResponse(BaseModel):

    status: str
    message: str


class SourceReference(BaseModel):

    source_file: str
    chunk_id: int
    similarity_score: float
    text_preview: str | None = None


class ChatRequest(BaseModel):

    query: str
    session_id: str


class ChatResponse(BaseModel):

    status: str
    answer: str
    sources: list[SourceReference]
    session_id: str | None = None