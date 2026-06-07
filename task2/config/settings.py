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

UPLOAD_FOLDER = os.getenv(
    "UPLOAD_FOLDER",
    "storage/uploads"
)