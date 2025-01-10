import time
import json
import os
from datetime import datetime

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
        self.data = {
            "seconds": [],
            "force": []
        }
        self.file_path = self.settings.get("graphSavePath")  
        
    def graphMeasure_timeLimit(self, Limit=1):
        self.Limit = Limit
        self.logger.log_info("Begining measurment process.")
        self.start_time = time.time()
        
        # Create a file with the current date and time in its name
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.file_name = f"measurement_{current_datetime}.json"
        self.full_file_path = os.path.join(self.file_path, self.file_name)
        
        self.timeLimit()

    def timeLimit(self):
        if time.time() - self.start_time < self.Limit:
            self.fc500.cmd_measure(silent=True)
            measurement = self.fc500.getLastResponse()
            
            elapsed_time = round(time.time() - self.start_time, 1000)
            self.data["seconds"].append(elapsed_time)
            self.data["force"].append(measurement.strip())

            with open(self.full_file_path, 'w') as f:
                json.dump(self.data, f, indent=4)

            QTimer.singleShot(1, lambda: (self.timeLimit()))
        else:
            self.logger.log_info("Measurment process finished.")