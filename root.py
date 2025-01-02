import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Qt
from gui_ui import Ui_Main
from ScreenController import ScreenControler
from PySide6.QtGui import QIcon
from EspCom import SerialCommunicator
from GraphControler import GraphControler
from settings import Settings


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Main()
        self.ui.setupUi(self)

        self.settings = Settings() #v02.01.25.1
        self.serial_communicator = SerialCommunicator(self.settings)
   
        self.setWindowTitle("Maszyna Wytrzymałościowa")
        self.setWindowIcon(QIcon(":/Menu/menu/Graph.png"))
        self.ui.Screen.setCurrentWidget(self.ui.Screen_Logo)
        self.graphControler = GraphControler(self.ui)

        self.screenControler = ScreenControler(self.ui, self.serial_communicator, self.settings) #v02.01.25.1 added self.settings
        self.screenControler.set_graph_controler(self.graphControler)

    def closeEvent(self, event):
        self.serial_communicator.close()
        self.settings.save_settings()
        event.accept()

        
#Running the app

app = QApplication(sys.argv)
MyApp = MainWindow()
MyApp.show()

MyApp.screenControler.ScreenSwitch_StartUp(MyApp.ui)

try:
    sys.exit(app.exec())
except SystemExit:
    print("[PBL MW]: Koniec")