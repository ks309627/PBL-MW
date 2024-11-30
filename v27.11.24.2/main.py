import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from ui import Ui_Main

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Main
        self.ui.setupUi(self)

app = QApplication(sys.argv)
MyApp = MainWindow()
MyApp.show()

try:
    sys.exit(app.exec())
except SystemExit:
    print("[PBL MW]: Koniec")