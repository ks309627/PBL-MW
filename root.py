import sys
import subprocess
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Qt
from gui_ui import Ui_Main
from PySide6.QtGui import QIcon, QFontDatabase, QFont
from ScreenController import ScreenControler
from settings import Settings
from LoggingHandler import Logger
from Measure_Lights import Measure_Lights
from FC500Com import FC500Com
from ESPCom import ESPCom #changed SerialCommunicator to ESPCom
from MeasureProcess_v2 import MeasureProcess

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        try:
            import matplotlib
        except ImportError:
            print("Dependencies not installed. Running setup script...")
            subprocess.check_call([sys.executable, "setup.py"])
            print("Dependencies installed. Restarting program...")
            os.execv(sys.executable, [sys.executable] + sys.argv)

        self.ui = Ui_Main()
        self.ui.setupUi(self)

        self.settings = Settings()
   
        self.setWindowTitle("Maszyna Wytrzymałościowa")
        self.setWindowIcon(QIcon(":/Menu/menu/Graph.png"))
        self.ui.Screen.setCurrentWidget(self.ui.Screen_MeasureMain)

    

        self.measure_process = MeasureProcess(self.ui, self.settings)

        self.screenControler = ScreenControler(self.ui, self.settings, self.measure_process)

        

        self.step_measure = Measure_Lights()

        self.FC500Com = FC500Com(self.settings)

        self.ESPCom = ESPCom(self.settings) #changed SerialCommunicator to ESPCom


    
        #v30.11.24.2
    def closeEvent(self, event):
        if hasattr(self.ESPCom, 'ser') and self.ESPCom.ser:
            self.ESPCom.connection_connection_close()
        if hasattr(self.FC500Com, 'ser') and self.FC500Com.ser:
            self.FC500Com.connection_close()
        self.settings.save_settings()
        event.accept()

        
#Running the app

error_logger = Logger()
error_logger.log_debug("=====================")
error_logger.log_debug("Uruchomienie Programu")
error_logger.log_debug("=====================")

app = QApplication(sys.argv)

font_id = QFontDatabase.addApplicationFont("Futura Std Book.ttf")

default_font = QFont("Futura Std Book", 10)
app.setFont(default_font)
MyApp = MainWindow()
MyApp.show()

MyApp.screenControler.ScreenSwitch_StartUp(MyApp.ui)

sys.exit(app.exec())
print("[PBL MW]: Koniec")