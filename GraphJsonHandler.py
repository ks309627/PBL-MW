import time
import json

from FC500Com import FC500Com
from LoggingHandler import Logger
from settings import Settings

class GraphRecorder:
    def __init__(self, settings:Settings):
        self.settings = settings
        self.fc500 = FC500Com(settings)
        self.logger = Logger()
        self.data = None
        self.data_list = []
        
    def graphMeasure_timeLimit(self, time=10):
        self.logger.log_info("Begining measurment process.")
        self.fc500.cmd_custom("Se1")
        start_time = time.time()
        try:
            while time.time() - start_time < time:
                self.data = self.fc500.getLastResponse()
                self.logger.log_debug(self.data)
        except Exception as e:
            self.logger.log_error(f"An error occured while trying to create graph: {e}")
        finally:
            self.fc500.cmd_custom("Se0")

    def graphMeasure_toggle(self, toggle_flag):
        pass