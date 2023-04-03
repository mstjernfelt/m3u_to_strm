import logging

class Logger:
    def __init__(self, provider= None):
        # Configure logging
        filename = f".local\\{provider}\\logfile.log"
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

        file_handler = logging.FileHandler(filename)
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)
