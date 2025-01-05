import logging
import sys
import threading
from PySide6.QtWidgets import QMessageBox
import traceback

class ErrorLogger:
    _instance = None
    _lock = threading.Lock()
    logger: logging.Logger
    file_handler: logging.FileHandler
    formatter: logging.Formatter

    def __new__(cls, log_file='error.log') -> 'ErrorLogger':
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ErrorLogger, cls).__new__(cls)
                cls._instance.logger = logging.getLogger(__name__)
                cls._instance.logger.setLevel(logging.DEBUG)
                cls._instance.file_handler = logging.FileHandler(log_file, encoding='utf-8')
                cls._instance.file_handler.setLevel(logging.DEBUG)
                cls._instance.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                cls._instance.file_handler.setFormatter(cls._instance.formatter)
                cls._instance.logger.addHandler(cls._instance.file_handler)
        return cls._instance

    def log_debug(self, message) -> None:
        self.logger.debug(message)

    def log_info(self, message):
        self.logger.info(message)
    
    def log_warning(self, message):
        self.logger.warning(message)
    
    def log_error(self, message):
        self.logger.error(message)

    def log_critical(self, message):
        self.logger.critical(message)

    def handle_exception(self, exc_type, exc_value, exc_traceback):
        self.logger.error(f"An error occured: {exc_type.__name__}: {exc_value}")
        self.logger.error("".join(traceback.format_tb(exc_traceback)))
        try:
            QMessageBox.critical(None, "Error", f"An error occured: {exc_type.__name__}: {exc_value}")
        except Exception as e:
            self.logger.error(f"Failed to show error message box: {e}")

def excepthook(exc_type, exc_value, exc_traceback):
    error_logger = ErrorLogger()
    error_logger.handle_exception(exc_type, exc_value, exc_traceback)

sys.excepthook = excepthook