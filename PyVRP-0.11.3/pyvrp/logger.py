import os
import logging
from datetime import datetime

def create_custom_logger(name: str, folder: str = "logs/pyvrp", filename_prefix: str = "run") -> logging.Logger:
    
    """
    Creates a logger writing to a timestamped log file in the given folder.
    """
    
    os.makedirs(folder, exist_ok=True)
    log_filename = f"{filename_prefix}_{datetime.now():%Y%m%d_%H%M%S}.log"
    log_path = os.path.join(folder, log_filename)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    file_handler = logging.FileHandler(log_path, mode='a', encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.log_path = log_path  # Optional: attach for retrieval
    return logger

