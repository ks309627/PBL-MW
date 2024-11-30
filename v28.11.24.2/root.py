import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from ui_gui import Ui_Main

class MyTest(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Main()
        self.ui.setupUi(self)    

app = QApplication(sys.argv)
MyApp = MyTest()
MyApp.show()

try:
    sys.exit(app.exec())
except SystemExit:
    print("Test")