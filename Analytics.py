import logging
import os
from datetime import datetime

def initialize_analytics():
    # Set up the logging configuration
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    print("Logging is initializing again!")

    log_filename = f"{log_dir}/analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    print(log_filename)

    # Remove any existing handlers from the root logger
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Create and configure a new FileHandler
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(formatter)

    # Create a new logger for the application
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    # Return the logger so it can be used for logging
    return logger

# Function to log entity movements
def log_entity_movement(entity_name, position, logger):
    logger.info(f"{entity_name} moved to position {position}")
