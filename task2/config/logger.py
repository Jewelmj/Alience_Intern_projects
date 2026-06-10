from pathlib import Path
import logging

from config.settings import (
    LOG_FOLDER,
    LOG_FILE,
    LOG_LEVEL
)

LOG_DIR = Path(LOG_FOLDER)
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / LOG_FILE,
    level=getattr(logging, LOG_LEVEL.upper()),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger("chat_engine")