import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Qt
from gui_ui import Ui_Main
from ScreenController import ScreenControler
# v30.11.24.2
from PySide6.QtGui import QIcon
from EspCom import SerialCommunicator

# v30.11.24.3
from GraphControler import GraphControler

# v02.01.24.1
from ErrorHandler import ErrorLogger

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Main()
        self.ui.setupUi(self)
   
        # v30.11.24.3 - added Window details
        self.setWindowTitle("Maszyna Wytrzymałościowa")
        self.setWindowIcon(QIcon(":/Menu/menu/Graph.png"))
        self.ui.Screen.setCurrentWidget(self.ui.Screen_Logo)
        # v30.11.24.3 - added Graph Controler
        self.graphControler = GraphControler(self.ui)

        # v30.11.24.2 - added serial_comunicator
        self.serial_communicator = SerialCommunicator()
        self.screenControler = ScreenControler(self.ui, self.serial_communicator)

        self.screenControler.set_graph_controler(self.graphControler)
    
        #v30.11.24.2
    def closeEvent(self, event):
        self.serial_communicator.close()
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