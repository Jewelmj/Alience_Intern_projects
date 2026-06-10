from io import BytesIO

from schema.utils.pdf_extraction import (
    extract_pdf_text
)
from schema.utils.file_storage import (
    save_extracted_text
)


class ExtractionAgent:

    def process(
        self,
        filename: str,
        content: bytes,
        max_pdf_pages: int
    ):

        text, page_count = extract_pdf_text(
            BytesIO(content)
        )

        if page_count > max_pdf_pages:

            raise ValueError(
                f"{filename} exceeds {max_pdf_pages} pages"
            )

        text_filename = save_extracted_text(
            filename,
            text
        )

        return {
            "page_count": page_count,
            "characters": len(text),
            "text_file": text_filename
        }