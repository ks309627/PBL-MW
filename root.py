import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Qt
from gui_ui import Ui_Main
from ScreenController import ScreenControler
from PySide6.QtGui import QIcon
from GraphControler import GraphControler
from settings import Settings
from LoggingHandler import Logger
from TerminalControler import TerminalControler
from Measure_Lights import Measure_Lights
from FC500Com import FC500Com
from ESPCom import ESPCom #changed SerialCommunicator to ESPCom

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Main()
        self.ui.setupUi(self)

        self.settings = Settings()
   
        self.setWindowTitle("Maszyna Wytrzymałościowa")
        self.setWindowIcon(QIcon(":/Menu/menu/Graph.png"))
        self.ui.Screen.setCurrentWidget(self.ui.Screen_Logo)
        self.graphControler = GraphControler(self.ui, self.settings)

        self.screenControler = ScreenControler(self.ui, self.settings)

        self.screenControler.set_graph_controler(self.graphControler)

        self.TerminalControler = TerminalControler(self.ui, self.settings)

        self.step_measure = Measure_Lights()

        self.FC500Com = FC500Com(self.settings)

        self.ESPCom = ESPCom(self.settings) #changed SerialCommunicator to ESPCom
    
        #v30.11.24.2
    def closeEvent(self, event):
        if hasattr(self.ESPCom, 'ser') and self.ESPCom.ser:
            self.ESPCom.connection_close()
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
MyApp = MainWindow()
MyApp.show()

MyApp.screenControler.ScreenSwitch_StartUp(MyApp.ui)

sys.exit(app.exec())
print("[PBL MW]: Koniec")