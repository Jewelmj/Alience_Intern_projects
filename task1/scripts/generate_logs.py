import os
import random

from datetime import datetime
from datetime import timedelta

from config.settings import (
    LOG_DIR,
    NUM_FILES,
    LOGS_PER_FILE,
    START_DATE,
    END_DATE,
)


LEVELS = ["INFO", "WARN", "ERROR"]

SERVICES = [
    "auth_service",
    "payment_service",
    "user_service",
    "notification_service",
    "search_service",
]

MESSAGES = {
    "INFO": [
        "Request completed in 120ms",
        "User logged in successfully",
        "Cache refreshed",
        "Connection established",
    ],
    "WARN": [
        "Retry attempt 1",
        "Slow response observed",
        "Rate limit nearing threshold",
    ],
    "ERROR": [
        "Timeout occurred",
        "Database connection failed",
        "Authentication failed",
        "Service unavailable",
    ]
}


def generate_random_timestamp(start_time, end_time):
    delta = end_time - start_time

    random_seconds = random.randint(
        0,
        int(delta.total_seconds())
    )

    return start_time + timedelta(
        seconds=random_seconds
    )

def choose_level():
    return random.choices(
        LEVELS,
        weights=[70, 20, 10],
        k=1
    )[0]

def generate_log_line(timestamp):
    level = choose_level()

    service = random.choice(SERVICES)

    message = random.choice(MESSAGES[level])

    return (
        f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} | "
        f"{level} | "
        f"{service} | "
        f"{message}"
    )


def generate_logs():
    os.makedirs(
        LOG_DIR,
        exist_ok=True
    )

    start_time = datetime.strptime(
        START_DATE,
        "%Y-%m-%d %H:%M:%S"
    )

    end_time = datetime.strptime(
        END_DATE,
        "%Y-%m-%d %H:%M:%S"
    )

    for file_number in range(1, NUM_FILES + 1):
        file_path = os.path.join(
            LOG_DIR,
            f"app_{file_number}.log"
        )

        print(f"Generating {file_path}...")

        with open(file_path, "w") as file:

            for _ in range(LOGS_PER_FILE):

                timestamp = generate_random_timestamp(
                    start_time,
                    end_time
                )

                log_line = generate_log_line(timestamp)

                file.write(log_line + "\n")

        print(f"Finished {file_path}")

if __name__ == "__main__":
    generate_logs()