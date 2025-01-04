import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Qt
from gui_ui import Ui_Main
from ScreenController import ScreenControler
from PySide6.QtGui import QIcon
from EspCom import SerialCommunicator
from GraphControler import GraphControler
from settings import Settings

# v02.01.24.1
from LoggingHandler import ErrorLogger

from TerminalControler import TerminalControler

from Measure_ProgressBar import Step_Measure

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Main()
        self.ui.setupUi(self)

        self.settings = Settings()
        self.serial_communicator = SerialCommunicator(self.settings)
   
        self.setWindowTitle("Maszyna Wytrzymałościowa")
        self.setWindowIcon(QIcon(":/Menu/menu/Graph.png"))
        self.ui.Screen.setCurrentWidget(self.ui.Screen_Logo)
        self.graphControler = GraphControler(self.ui, self.settings)

        # v30.11.24.2 - added serial_comunicator
        #self.serial_communicator = SerialCommunicator() 
        self.screenControler = ScreenControler(self.ui, self.serial_communicator, self.settings)

        self.screenControler.set_graph_controler(self.graphControler)

        self.TerminalControler = TerminalControler(self.ui)

        self.step_measure = Step_Measure()
    
        #v30.11.24.2
    def closeEvent(self, event):
        self.serial_communicator.close()
        self.settings.save_settings()
        event.accept()

        
#Running the app

error_logger = ErrorLogger()
error_logger.log_debug("Uruchomienie Programu")

app = QApplication(sys.argv)
MyApp = MainWindow()
MyApp.show()

MyApp.screenControler.ScreenSwitch_StartUp(MyApp.ui)

sys.exit(app.exec())
print("[PBL MW]: Koniec")