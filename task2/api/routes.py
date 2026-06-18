from pathlib import Path
from typing import Union
from fastapi import APIRouter, UploadFile, File

from config.settings import (
    MAX_UPLOAD_FILES,
    UPLOAD_FOLDER,
    EXTRACTED_TEXT_FOLDER
)
from config.logger import logger

from schema.models.response import (
    UploadResponse,
    HomeResponse,
    ErrorResponse,
    ChatRequest,
    ChatResponse
)

from dependencies.agents import (
    ingestion_agent,
    retrieval_agent
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


@router.get("/",response_model=HomeResponse)
def home():
    return {"message": "API is running"}


@router.post("/upload",response_model=Union[UploadResponse,ErrorResponse])
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
            logger.exception(
                f"Failed to process {file.filename}: {e}"
            )

            return {
                "status": "error",
                "message": str(e)
            }
    
    logger.info(
        f"Upload completed successfully. Saved {len(saved_files)} file(s)"
    )

    return {
        "status": "success",
        "files": saved_files
    }


@router.post(
    "/chat",
    response_model=Union[ChatResponse, ErrorResponse]
)
def chat(
    request: ChatRequest
):

    logger.info(
        f"Chat request received: {request.query!r}"
    )

    try:

        result = retrieval_agent.chat(
            request.query
        )

    except ValueError as exc:

        logger.warning(str(exc))

        return {
            "status": "error",
            "message": str(exc)
        }

    except Exception as exc:

        logger.exception(
            f"Chat request failed: {exc}"
        )

        return {
            "status": "error",
            "message": str(exc)
        }

    result["session_id"] = request.session_id

    return result