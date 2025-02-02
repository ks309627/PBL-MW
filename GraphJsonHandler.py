import time
import json
import os
from datetime import datetime

from PySide6.QtCore import QTimer

from GraphControler import GraphControler
from GraphList import GraphList
from FC500Com import FC500Com
from LoggingHandler import Logger
from settings import Settings
from gui_ui import Ui_Main

try:
    import matplotlib.pyplot as plt
except Exception as e:
    print(f"An error occured when starting up! {e}. Some functionality of the program might not work properly! Usage of the program is a risk!")

class GraphRecorder:
    def __init__(self, gui:Ui_Main, settings:Settings):
        self.settings = settings
        self.fc500 = FC500Com(settings)
        self.logger = Logger()
        self.graph_controler = GraphControler(gui, settings)
        self.graph_icons = GraphList(gui, settings)
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

        self.current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        if Limit == 'unlimited': #begin an infinite measurement. USE WITH CAUTION!
            self.Limit = 'unlimited'
            self.paused = False
            self.logger.log_info("Begining unlimited measurment process.")
            self.start_time = time.time()
            
            self.file_name_json = f"measurement_{self.current_datetime}.json"
            self.folder_name = f"measurement_{self.current_datetime}"
            self.full_file_path = os.path.join(self.file_path, self.folder_name, self.file_name_json)
            self.graph_icons.load_graphs()

            os.makedirs(os.path.join(self.file_path, self.folder_name), exist_ok=True)
            
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
            
            
            self.file_name_json = f"measurement_{self.current_datetime}.json"
            self.folder_name = f"measurement_{self.current_datetime}"
            self.full_file_path = os.path.join(self.file_path, self.folder_name, self.file_name_json)
            self.graph_icons.load_graphs()

            os.makedirs(os.path.join(self.file_path, self.folder_name), exist_ok=True)
            
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
                self.create_icon()
                self.graph_icons.load_graphs()
        else:
            if hasattr(self, 'start_time'):
                del self.start_time  # Remove the start time attribute
            QTimer.singleShot(100, lambda: (self.check_status()))

    def check_status(self):
        if self.paused:
            QTimer.singleShot(100, lambda: (self.check_status()))
        else:
            return
        
    def create_icon(self):
        try:
            image_size = (80, 60)
            dpi = 100
            plt.figure(figsize=(image_size[0] / dpi, image_size[1] / dpi), dpi=dpi)
            plt.xticks([])
            plt.yticks([])
            plt.axis('off')

            forces = []
            for f in self.data["force"]:
                f = f.replace("N", "").strip()
                if "-" in f:
                    forces.append(-float(f.replace("-", "").strip()))
                else:
                    forces.append(float(f))

            plt.plot(self.data["seconds"], forces)
            self.file_name_icon = f"icon_{self.current_datetime}.jpeg"
            image_path = os.path.join(self.file_path, self.folder_name, self.file_name_icon)
            plt.savefig(image_path, bbox_inches="tight")
            plt.close()
        except Exception as e:
            self.logger.log_error(f"Image creation failed! {e}")
            return
