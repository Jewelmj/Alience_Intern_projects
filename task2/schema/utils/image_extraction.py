from io import BytesIO
from config.logger import logger

import easyocr
import numpy as np
from PIL import Image

reader = None

def get_reader():
    global reader

    if reader is None:

        logger.info(
            "Initializing EasyOCR"
        )

        reader = easyocr.Reader(
            ["en"]
        )

    return reader

def extract_image_text(content: bytes):

    logger.info("Opening image")

    try:
        image = Image.open(
            BytesIO(content)
        )
    except Exception as e:
        logger.error(f"Failed to open image: {e}")
        raise ValueError("Invalid image file")

    logger.info("Running OCR")

    result = get_reader().readtext(
        np.array(image)
    )

    logger.info(
        f"OCR detected {len(result)} text regions"
    )

    text = "\n".join(
        item[1]
        for item in result
    )

    logger.info(
        f"OCR extracted {len(text)} characters"
    )

    return text