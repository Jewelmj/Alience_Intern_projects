import os

from datetime import datetime

def parse_log_line(line):
    try:
        parts = line.strip().split(" | ")

        if len(parts) != 4:
            return None

        timestamp_str, level, service, message = parts

        timestamp = datetime.strptime(
            timestamp_str,
            "%Y-%m-%d %H:%M:%S"
        )

        return {
            "timestamp": timestamp,
            "level": level,
            "service": service,
            "message": message
        }

    except Exception:
        return None
    
def parse_log_file(file_path):
    with open(file_path, "r") as file:

        for line in file:

            parsed_log = parse_log_line(line)

            if parsed_log is not None:
                yield parsed_log

def parse_log_directory(log_dir):
    for file_name in os.listdir(log_dir):

        if file_name.endswith(".log"):

            file_path = os.path.join(
                log_dir,
                file_name
            )

            yield from parse_log_file(
                file_path
            )