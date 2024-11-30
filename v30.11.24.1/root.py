import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import Qt, QIcon
from gui_ui import Ui_Main
from ScreenController import ScreenControler
from GraphControler import GraphControler

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Main()
        self.ui.setupUi(self)
        self.setWindowTitle("Maszyna Wytrzymałościowa")
        self.setWindowIcon(QIcon(":/Menu/menu/Graph.png"))
        self.ui.Screen.setCurrentWidget(self.ui.Screen_Logo)
        self.screenControler = ScreenControler(self.ui)
        self.grapphControler = GraphControler()

#Running the app

app = QApplication(sys.argv)
MyApp = MainWindow()
MyApp.show()

MyApp.screenControler.ScreenSwitch_StartUp(MyApp.ui)

try:
    sys.exit(app.exec())
except SystemExit:
    print("[PBL MW]: Koniec")