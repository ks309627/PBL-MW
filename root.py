import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Qt, QTimer
from gui_ui import Ui_Main
from ScreenController import ScreenControler
# \/ v30.11.24.2
from EspCom import SerialCommunicator
from PySide6.QtCore import QTimer
# /\ v30.11.24.2



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Main()
        self.ui.setupUi(self)

        # \/ v30.11.24.2
        self.serial_communicator = SerialCommunicator()
        self.screenControler = ScreenControler(self.ui, self.serial_communicator) #added serial_comunicator v30.11.24.2
    
    def closeEvent(self, event):
        self.serial_communicator.close()
        event.accept()
        # /\ v30.11.24.2
        
#Running the app

app = QApplication(sys.argv)
MyApp = MainWindow()
MyApp.show()

MyApp.screenControler.ScreenSwitch_StartUp(MyApp.ui)

try:
    sys.exit(app.exec())
except SystemExit:
    print("[PBL MW]: Koniec")