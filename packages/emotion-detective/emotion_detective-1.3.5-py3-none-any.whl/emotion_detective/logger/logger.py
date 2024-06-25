import os
import logging

def setup_logging():
    """
    Sets up logging for the application.

    This function configures a logger to output log messages to
    both a file and the console.
    The log messages include a timestamp, the log level, and the message.

    The log file is saved as 'logs/emotion_detective.txt'.

    Returns:
        logging.Logger: Configured logger instance.
    """
    # Set up logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Set default logging level to DEBUG

    # Check if logs folder exists, create if it doesn't
    logs_folder = 'logs'
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)

    # Check if log file exists, create if it doesn't
    log_file = os.path.join(logs_folder, 'emotion_detective.txt')
    if not os.path.exists(log_file):
        with open(log_file, 'w'):
            pass

    # Create file handler and set formatter
    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # Create console handler and set formatter
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Optionally, add error logging to a separate file
    error_file_handler = logging.FileHandler(os.path.join(logs_folder, 'error.log'))
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    logger.addHandler(error_file_handler)

    return logger
