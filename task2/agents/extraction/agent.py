from io import BytesIO
from pathlib import Path

from schema.utils.pdf_extraction import (
    extract_pdf_text
)
from schema.utils.image_extraction import (
    extract_image_text
)
from schema.utils.file_storage import (
    save_extracted_text
)
from config.logger import logger


class ExtractionAgent:

    def process(
        self,
        filename: str,
        content: bytes,
        max_pdf_pages: int
    ):

        extension = Path(filename).suffix.lower()

        if extension == ".pdf":

            text, page_count = extract_pdf_text(
                BytesIO(content)
            )

            if page_count > max_pdf_pages:

                raise ValueError(
                    f"{filename} exceeds {max_pdf_pages} pages"
                )

        elif extension in [
            ".png",
            ".jpg",
            ".jpeg"
        ]:
            logger.info(
        f"Starting OCR for {filename}"
            )

            text = extract_image_text(
                content
            )

            logger.info(
                f"OCR extracted text: {text}"
            )

            page_count = None

            logger.info(
        f"Saving extracted text..."
    )

        else:

            raise ValueError(
                f"Unsupported file type: {filename}"
            )

        text_filename = save_extracted_text(
            filename,
            text
        )

        logger.info(
        f"Text saved successfully: {text_filename}"
    )

        return {
            "page_count": page_count,
            "characters": len(text),
            "text_file": text_filename
        }