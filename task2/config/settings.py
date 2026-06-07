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