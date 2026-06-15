import os

from dotenv import load_dotenv

load_dotenv()

ALLOWED_EXTENSIONS = set(
    os.getenv(
        "ALLOWED_EXTENSIONS",
        ".pdf,.png,.jpg,.jpeg"
    ).split(",")
)

MAX_UPLOAD_FILES = int(
    os.getenv(
        "MAX_UPLOAD_FILES",
        3
    )
)

MAX_PDF_PAGES = int(
    os.getenv(
        "MAX_PDF_PAGES",
        5
    )
)

UPLOAD_FOLDER = os.getenv(
    "UPLOAD_FOLDER",
    "storage/uploads"
)

LOG_FOLDER = os.getenv(
    "LOG_FOLDER",
    "logs"
)

LOG_FILE = os.getenv(
    "LOG_FILE",
    "app.log"
)

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)

EXTRACTED_TEXT_FOLDER = os.getenv(
    "EXTRACTED_TEXT_FOLDER",
    "storage/extracted_text"
)

CHUNK_SIZE = int(
    os.getenv(
        "CHUNK_SIZE",
        500
    )
)

CHUNK_OVERLAP = int(
    os.getenv(
        "CHUNK_OVERLAP",
        100
    )
)