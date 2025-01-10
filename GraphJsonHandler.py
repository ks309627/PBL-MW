import time

from PySide6.QtCore import QTimer

from FC500Com import FC500Com
from LoggingHandler import Logger
from settings import Settings

class GraphRecorder:


    def __init__(self, settings:Settings):
        self.settings = settings
        self.fc500 = FC500Com(settings)
        self.logger = Logger()
        self.start_time = None
        self.data = None
        self.timeLimit = None
        self.data_list = []
        
    def graphMeasure_timeLimit(self, timeLimit=1):
        self.timeLimit = timeLimit 
        self.logger.log_info("Begining measurment process.")
        self.start_time = time.time()
        self.timeLimit_loop()
        
    def timeLimit_loop(self):
        QTimer.singleShot(1000, lambda: (self.timeLimit_action()))

    def timeLimit_action(self):
        if time.time() - self.start_time < self.timeLimit:
            self.fc500.cmd_measure()
            self.data = self.fc500.getLastResponse()
            self.logger.log_debug(self.data)