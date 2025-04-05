import logging
import os

class CustomLogger:
    def __init__(self, log_file_name):
        """
        Initializes the logger with the specified log file name.

        Args:
            log_file_name (str): The name of the log file where logs will be written.
        """
        # Ensure the directory for the log file exists
        log_dir = os.path.dirname(log_file_name)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Configure the logger
        logging.basicConfig(
            filename=log_file_name,
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - [%(module)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)

    def get_logger(self):
        """
        Returns the logger instance.

        Returns:
            logging.Logger: The configured logger instance.
        """
        return self.logger