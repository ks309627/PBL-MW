import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow,QWidget
from testgui import Ui_Form
class MyQTApp(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.Input.setText("Hello World!")
        self.ui.Button.clicked.connect(self.say_hello)
        self.Text=str()
    def say_hello(self):
        input_Text = self.ui.Input.text()
        if(not self.Text==""):
            self.Text=self.Text+'\n'+input_Text
        else:
            self.Text=input_Text
        self.ui.Output.setText(self.Text)

app = QApplication(sys.argv)
MyApp = MyQTApp()
MyApp.show()

try:
    sys.exit(app.exec())
except SystemExit:
    print("[GUI]: Koniec")