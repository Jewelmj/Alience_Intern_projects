from pypdf import PdfReader
from pathlib import Path

from config.settings import (
    EXTRACTED_TEXT_FOLDER
)

def get_unique_filename(file_path: Path) -> Path:
    """
    Prevent overwriting existing files.
    Example:
        report.pdf
        report_1.pdf
        report_2.pdf
    """

    if not file_path.exists():
        return file_path

    stem = file_path.stem
    suffix = file_path.suffix

    counter = 1

    while True:

        new_path = (
            file_path.parent
            / f"{stem}_{counter}{suffix}"
        )

        if not new_path.exists():
            return new_path

        counter += 1

def save_extracted_text(
    filename: str,
    text: str
):
    txt_path = (
        Path(EXTRACTED_TEXT_FOLDER)
        / f"{Path(filename).stem}.txt"
    )

    with open(
        txt_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(text)

    return txt_path.name