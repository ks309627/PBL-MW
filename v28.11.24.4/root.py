import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Qt, QTimer
from gui_ui import Ui_Main
from ScreenController import ScreenControler

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Main()
        self.ui.setupUi(self)
        self.screenControler = ScreenControler(self.ui)

#Running the app

app = QApplication(sys.argv)
MyApp = MainWindow()
MyApp.show()

MyApp.screenControler.ScreenSwitch_StartUp(MyApp.ui)

try:
    sys.exit(app.exec())
except SystemExit:
    print("[PBL MW]: Koniec")