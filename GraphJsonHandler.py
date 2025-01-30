import time
import json
import os
from datetime import datetime

from PySide6.QtCore import QTimer

from GraphControler import GraphControler
from FC500Com import FC500Com
from LoggingHandler import Logger
from settings import Settings
from gui_ui import Ui_Main

class GraphRecorder:
    def __init__(self, gui:Ui_Main, settings:Settings):
        self.settings = settings
        self.fc500 = FC500Com(settings)
        self.logger = Logger()
        self.graph_controler = GraphControler(gui, settings)
        self.start_time = None
        self.data = {
            "seconds": [],
            "force": []
        }
        self.file_path = self.settings.get("graphSavePath")  
        
    def graphMeasure_process(self, Limit=1):
        self.data = {
            "seconds": [],
            "force": []
        }

        if Limit == 'unlimited': #begin an infinite measurement. USE WITH CAUTION!
            self.Limit = 'unlimited'
            self.paused = False
            self.logger.log_info("Begining unlimited measurment process.")
            self.start_time = time.time()
            
            current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.file_name = f"measurement_{current_datetime}.json"
            self.full_file_path = os.path.join(self.file_path, self.file_name)
            
            self.timeLimit()

        if Limit == 'reset': #force reset timer and stop it
            self.Limit = 1
            self.paused = True
            self.data = {
                "seconds": [],
                "force": []
            }
            if hasattr(self, 'start_time'):
                del self.start_time
            return
        
        if Limit == 'stop': #pause the timer
            self.paused = True

        if Limit == 'start': #unpause
            self.paused = False
            self.start_time = time.time() - (time.time() - self.start_time) if hasattr(self, 'start_time') else time.time()
            self.timeLimit()

        if Limit not in ['stop', 'start', 'reset']:
            self.Limit = Limit
            self.paused = False
            self.logger.log_info("Begining measurment process.")
            self.start_time = time.time()
            
            current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.file_name = f"measurement_{current_datetime}.json"
            self.full_file_path = os.path.join(self.file_path, self.file_name)
            
            self.timeLimit()

    def timeLimit(self):
        if not hasattr(self, 'paused') or not self.paused:
            if self.Limit == 'unlimited' or time.time() - self.start_time < self.Limit:
                self.fc500.cmd_measure(silent=True)
                measurement = self.fc500.getLastResponse()
                
                elapsed_time = round(time.time() - self.start_time, 1000)
                self.data["seconds"].append(elapsed_time)
                self.data["force"].append(measurement.strip())

                with open(self.full_file_path, 'w') as f:
                    json.dump(self.data, f, indent=4)

                self.graph_controler.default_load()
                QTimer.singleShot(1, lambda: (self.timeLimit()))
            else:
                self.logger.log_info("Measurment process finished.")
        else:
            if hasattr(self, 'start_time'):
                del self.start_time  # Remove the start time attribute
            QTimer.singleShot(100, lambda: (self.check_status()))

    def check_status(self):
        if self.paused:
            QTimer.singleShot(100, lambda: (self.check_status()))
        else:
            return