from src.parser import parse_log_directory

from config.settings import LOG_DIR


for log in parse_log_directory(LOG_DIR):

    print(log)

    break