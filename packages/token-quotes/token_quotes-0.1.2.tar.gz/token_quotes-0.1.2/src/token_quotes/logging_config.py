# logging_config.py
import logging
import os
from datetime import datetime


def setup_logging():
    # Ensure the log directory exists
    LOG_DIR = "./logs"
    os.makedirs(LOG_DIR, exist_ok=True)

    # Create a timestamp for the log file name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(LOG_DIR, f"app_log_{timestamp}.log")

    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(),  # This will output to stdout/stderr
        ],
    )


# Call setup_logging at the module level
setup_logging()
