import logging
import os

LOGS_FOLDER = 'logs'
os.makedirs(LOGS_FOLDER, exist_ok=True)

def setup_logger(name: str, filename: str, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)


    if not logger.handlers:
        file_handler = logging.FileHandler(os.path.join(LOGS_FOLDER, filename), encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    logger.propagate = False

    return logger
