import os
from dotenv import load_dotenv

load_dotenv()

LOG_DIR = os.getenv("LOG_DIR", "logs")

NUM_FILES = int(
    os.getenv("NUM_FILES", 5)
)

LOGS_PER_FILE = int(
    os.getenv("LOGS_PER_FILE", 100000)
)

START_DATE = os.getenv(
    "START_DATE",
    "2026-03-18 00:00:00"
)

END_DATE = os.getenv(
    "END_DATE",
    "2026-03-19 00:00:00"
)

ANOMALY_THRESHOLD = int(
    os.getenv("ANOMALY_THRESHOLD", 50)
)

OUTPUT_DIR = os.getenv(
    "OUTPUT_DIR",
    "output"
)

OUTPUT_FILE = os.getenv(
    "OUTPUT_FILE",
    "result.json"
)