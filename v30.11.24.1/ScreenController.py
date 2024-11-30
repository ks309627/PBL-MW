from gui_ui import Ui_Main
from PySide6.QtCore import QTimer

class ScreenControler:
    def __init__(self, gui:Ui_Main):

            #Screen switch buttons
        gui.btn_Measure.clicked.connect(lambda: gui.Screen.setCurrentWidget(gui.Screen_MeasureMain))
        gui.btn_Graphs.clicked.connect(lambda: gui.Screen.setCurrentWidget(gui.Screen_Graphs))
        gui.btn_Settings.clicked.connect(lambda: gui.Screen.setCurrentWidget(gui.Screen_Settings))
        gui.btn_Errors.clicked.connect(lambda: gui.Screen.setCurrentWidget(gui.Screen_Errors))
        
        gui.btn_MeasureToGraph.clicked.connect(lambda: (gui.Screen.setCurrentWidget(gui.Screen_Graphs), self.ScreenSwitch_CategoryGraphs(gui)))
        gui.btn_StartMeasure.clicked.connect(lambda: (gui.Screen.setCurrentWidget(gui.Screen_MeasureProgress), self.ScreenSwitch_CategoryMeasure(gui)))
        gui.btn_StopMeasure.clicked.connect(lambda: (gui.Screen.setCurrentWidget(gui.Screen_MeasureMain), self.ScreenSwitch_CategoryMeasure(gui)))

        #Additional Screen swtich actions
    def ScreenSwitch_StartUp(self, gui:Ui_Main):
        gui.Menu.setStyleSheet("background-color: rgb(255, 255, 255);")
        gui.Menu.setVisible(0)
        QTimer.singleShot(1000, lambda:
            (gui.Menu.setVisible(1),
             gui.btn_Measure.setChecked(1),
             gui.Screen.setCurrentWidget(gui.Screen_MeasureMain),
             gui.Menu.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0.0113636 rgba(225, 225, 225, 255), stop:1 rgba(245, 245, 245, 255));")
             ))

    def ScreenSwitch_CategoryMeasure(self, gui:Ui_Main):
        gui.btn_Measure.setChecked(1)
        gui.btn_Graphs.setChecked(0)
        gui.btn_Settings.setChecked(0)
        gui.btn_Errors.setChecked(0)

    def ScreenSwitch_CategoryGraphs(self, gui:Ui_Main):
        gui.btn_Measure.setChecked(0)
        gui.btn_Graphs.setChecked(1)
        gui.btn_Settings.setChecked(0)
        gui.btn_Errors.setChecked(0)

    def ScreenSwitch_CategorySettings(self, gui:Ui_Main):
        gui.btn_Measure.setChecked(0)
        gui.btn_Graphs.setChecked(0)
        gui.btn_Settings.setChecked(1)
        gui.btn_Errors.setChecked(0)

    def ScreenSwitch_CategoryErrors(self, gui:Ui_Main):
        gui.btn_Measure.setChecked(0)
        gui.btn_Graphs.setChecked(0)
        gui.btn_Settings.setChecked(0)
        gui.btn_Errors.setChecked(1)