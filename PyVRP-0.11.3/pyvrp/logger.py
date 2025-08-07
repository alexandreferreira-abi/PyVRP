import os
import logging
from pathlib import Path


def create_custom_logger(
    name: str,
    folder: str = "logs/pyvrp",
    filename_prefix: str = "run",
    run_id: str | None = None,
) -> logging.Logger:
    
    """
    Creates a logger with a unique file name derived from a run_id.
    Also creates a companion .txt file to track the latest iteration.

    Parameters
    ----------
    name : str
        Name of the logger (must be unique per run).
    folder : str
        Folder where logs are stored.
    filename_prefix : str
        Prefix for the log and .txt file names.
    run_id : str
        Unique identifier for the run (includes timestamp). Required to ensure uniqueness.

    Returns
    -------
    logger : logging.Logger
        Logger with '.log_path' and '.latest_iter_path' attributes attached.
    """

    os.makedirs(folder, exist_ok=True)

    if not run_id:
        raise ValueError("run_id is required for unique file naming.")

    log_path = Path(folder) / f"{filename_prefix}_{run_id}.log"
    iter_txt_path = Path(folder) / f"{filename_prefix}_{run_id}_latest_iter.txt"

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler = logging.FileHandler(log_path, mode='a', encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Optional: console logging (you can skip this)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.log_path = log_path
    logger.latest_iter_path = iter_txt_path
    iter_txt_path.touch(exist_ok=True)

    logger.info("Logger initialized.")

    return logger


def get_null_logger(name="null"):
    
    """
    Returns a logger that silently ignores all log messages.

    This utility is useful as a fallback when no logger is explicitly provided,
    allowing logging calls to be safely executed without requiring setup.

    Parameters
    ----------
    name : str
        Name for the null logger. Default is "null".

    Returns
    -------
    logging.Logger
        A logger instance with a NullHandler, which discards all messages.
        The logger also has propagation disabled to prevent bubbling to root handlers.

    Notes
    -----
    - If the logger already has handlers, no new ones are added.
    - This is ideal for optional logging in library functions.
    """
    
    null_logger = logging.getLogger(name)
    null_logger.addHandler(logging.NullHandler())
    null_logger.propagate = False
    return null_logger
