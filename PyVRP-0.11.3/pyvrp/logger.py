import os
import logging
from datetime import datetime
from pathlib import Path

def create_custom_logger(name: str, folder: str = "logs/pyvrp", filename_prefix: str = "run") -> logging.Logger:
    """
    Creates a logger writing to a timestamped log file (no console),
    and attaches a `latest_iter_path` attribute to the logger for tracking.
    """
    os.makedirs(folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"{filename_prefix}_{timestamp}.log"
    log_path = os.path.join(folder, log_filename)

    # === Create logger ===
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler = logging.FileHandler(log_path, mode='a', encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # === Create companion .txt path for latest iteration tracking ===
    iter_txt_path = Path(folder) / f"{filename_prefix}_{timestamp}_latest_iter.txt"
    iter_txt_path.touch(exist_ok=True)

    # === Attach attributes to logger ===
    logger.log_path = Path(log_path)
    logger.latest_iter_path = iter_txt_path

    return logger
