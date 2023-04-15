import logging

class Logger:
    verbose = False

    def __init__(self, provider= None, in_verbose = False):
        # Configure logging
        self.verbose = in_verbose
        filename = f".local/{provider}/logfile.log"
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

        file_handler = logging.FileHandler(filename, encoding="UTF-8")
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def debug(self, message):
        self.logger.debug(message)
        if self.verbose:
            print(f"DEBUG: {message}")

    def info(self, message):
        self.logger.info(message)
        if self.verbose:
            print(f"INFO: {message}")

    def warning(self, message):
        self.logger.warning(message)
        if self.verbose:
            print(f"WARNING: {message}")

    def error(self, message):
        self.logger.error(message)
        if self.verbose:
            print(f"ERROR: {message}")

    def critical(self, message):
        self.logger.critical(message)
        if self.verbose:
            print(f"CRITICAL: {message}")
