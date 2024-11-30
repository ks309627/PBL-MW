import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Qt, QTimer
from gui_ui import Ui_Main


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Main()
        self.ui.setupUi(self)

        # self.ScreenSwitch_StartUp()

        #Screen switch buttons
        self.ui.btn_Measure.clicked.connect(lambda: (self.ui.Screen.setCurrentWidget(self.ui.Screen_MeasureMain), self.ScreenSwitch_CategoryMeasure()))
        self.ui.btn_Graphs.clicked.connect(lambda: (self.ui.Screen.setCurrentWidget(self.ui.Screen_Graphs), self.ScreenSwitch_CategoryGraphs()))
        self.ui.btn_Settings.clicked.connect(lambda: (self.ui.Screen.setCurrentWidget(self.ui.Screen_Settings), self.ScreenSwitch_CategorySettings()))
        self.ui.btn_Errors.clicked.connect(lambda: (self.ui.Screen.setCurrentWidget(self.ui.Screen_Errors), self.ScreenSwitch_CategoryErrors()))
        self.ui.btn_MeasureToGraph.clicked.connect(lambda: (self.ui.Screen.setCurrentWidget(self.ui.Screen_Graphs), self.ScreenSwitch_CategoryGraphs()))
        self.ui.btn_StartMeasure.clicked.connect(lambda: (self.ui.Screen.setCurrentWidget(self.ui.Screen_MeasureProgress), self.ScreenSwitch_CategoryMeasure()))
        self.ui.btn_StopMeasure.clicked.connect(lambda: (self.ui.Screen.setCurrentWidget(self.ui.Screen_MeasureMain), self.ScreenSwitch_CategoryMeasure()))

        #Additional Screen swtich actions
    # def ScreenSwitch_StartUp(self):
    #     self.ui.Menu.setVisible(0)
    #     QTimer.singleShot(2000, self.ui.Menu.setVisible(1))
    #     self.ui.btn_Measure.setChecked(1)
    #     self.ui.Screen.setCurrentWidget(self.ui.Screen_MeasureMain)

    def ScreenSwitch_CategoryMeasure(self):
        self.ui.btn_Measure.setChecked(1)
        self.ui.btn_Graphs.setChecked(0)
        self.ui.btn_Settings.setChecked(0)
        self.ui.btn_Errors.setChecked(0)

    def ScreenSwitch_CategoryGraphs(self):
        self.ui.btn_Measure.setChecked(0)
        self.ui.btn_Graphs.setChecked(1)
        self.ui.btn_Settings.setChecked(0)
        self.ui.btn_Errors.setChecked(0)

    def ScreenSwitch_CategorySettings(self):
        self.ui.btn_Measure.setChecked(0)
        self.ui.btn_Graphs.setChecked(0)
        self.ui.btn_Settings.setChecked(1)
        self.ui.btn_Errors.setChecked(0)

    def ScreenSwitch_CategoryErrors(self):
        self.ui.btn_Measure.setChecked(0)
        self.ui.btn_Graphs.setChecked(0)
        self.ui.btn_Settings.setChecked(0)
        self.ui.btn_Errors.setChecked(1)

    #Running the app

app = QApplication(sys.argv)
MyApp = MainWindow()
MyApp.show()



try:
    sys.exit(app.exec())
except SystemExit:
    print("[PBL MW]: Koniec")