import logging
import sys
import threading
from PySide6.QtWidgets import QMessageBox
import traceback
import datetime
import os

logging.USER = 25
logging.addLevelName(logging.USER, "USER")

class ErrorLogger:
    _instance = None
    _lock = threading.Lock()
    logger: logging.Logger
    file_handler: logging.FileHandler
    formatter: logging.Formatter
    log_dir: str
    max_files: int
    join_files: int

    def __new__(cls, log_dir='logs') -> 'ErrorLogger':
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ErrorLogger, cls).__new__(cls)
                cls._instance.logger = logging.getLogger(__name__)
                cls._instance.logger.setLevel(logging.DEBUG)
                cls._instance.log_dir = log_dir
                cls._instance.max_files = 20
                cls._instance.join_files = 5
                if not os.path.exists(log_dir):
                    os.makedirs(log_dir)
                cls._instance._clean_up_old_logs()
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                log_file = f'{log_dir}/log_{timestamp}.log'
                cls._instance.file_handler = logging.FileHandler(log_file, encoding="utf-8")
                cls._instance.file_handler.setLevel(logging.DEBUG)
                cls._instance.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                cls._instance.file_handler.setFormatter(cls._instance.formatter)
                cls._instance.logger.addHandler(cls._instance.file_handler)
        return cls._instance

    def log_user(self, message):
        self.logger.log(logging.USER, message)

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

    def _clean_up_old_logs(self):
        log_files = [f for f in os.listdir(self.log_dir) if f.startswith('log_') and f.endswith('.log')]
        log_files.sort()
        if len(log_files) >= self.max_files:
            old_files = log_files[:len(log_files) - self.max_files + 1]
            for file in old_files:
                os.remove(os.path.join(self.log_dir, file))

    def join_logs(self, output_file):
        if os.path.exists(output_file):
            os.remove(output_file)
        log_files = [f for f in os.listdir(self.log_dir) if f.startswith('log_') and f.endswith('.log')]
        log_files.sort(reverse=True)
        with open(output_file, 'w') as output:
            for file in log_files[:self.join_files]:  # Use join_files instance variable
                with open(os.path.join(self.log_dir, file), 'r') as log_file:
                    output.write(log_file.read())
                    output.write('\n\n')

def excepthook(exc_type, exc_value, exc_traceback):
    error_logger = ErrorLogger()
    error_logger.handle_exception(exc_type, exc_value, exc_traceback)

sys.excepthook = excepthook