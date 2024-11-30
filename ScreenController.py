from gui_ui import Ui_Main
from PySide6.QtCore import QTimer
# \/ v30.11.24.2
from EspCom import SerialCommunicator
# /\ v30.11.24.2

class ScreenControler:
    def __init__(self, gui:Ui_Main, communicator): #added comunicator v30.11.24.2
    #Screen switch buttons
        gui.btn_Measure.clicked.connect(lambda: (gui.Screen.setCurrentWidget(gui.Screen_MeasureMain), self.ScreenSwitch_CategoryMeasure(gui)))
        gui.btn_Graphs.clicked.connect(lambda: (gui.Screen.setCurrentWidget(gui.Screen_Graphs), self.ScreenSwitch_CategoryGraphs(gui)))
        gui.btn_Settings.clicked.connect(lambda: (gui.Screen.setCurrentWidget(gui.Screen_Settings), self.ScreenSwitch_CategorySettings(gui)))
        gui.btn_Errors.clicked.connect(lambda: (gui.Screen.setCurrentWidget(gui.Screen_Errors), self.ScreenSwitch_CategoryErrors(gui)))
        gui.btn_MeasureToGraph.clicked.connect(lambda: (gui.Screen.setCurrentWidget(gui.Screen_Graphs), self.ScreenSwitch_CategoryGraphs(gui)))
        gui.btn_StartMeasure.clicked.connect(lambda: (gui.Screen.setCurrentWidget(gui.Screen_MeasureProgress), self.ScreenSwitch_CategoryMeasure(gui)))
        gui.btn_StopMeasure.clicked.connect(lambda: (gui.Screen.setCurrentWidget(gui.Screen_MeasureMain), self.ScreenSwitch_CategoryMeasure(gui)))

        # \/ v30.11.24.2
        self.gui = gui
        self.communicator = communicator
        gui.pushButton.clicked.connect(self.send_left_command)
        gui.pushButton_2.clicked.connect(self.send_right_command)
        gui.pushButton_3.clicked.connect(self.connect)
        # /\ v30.11.24.2

        #Additional Screen swtich actions
    def ScreenSwitch_StartUp(self, gui:Ui_Main):
        gui.Menu.setStyleSheet("background-color: rgb(255, 255, 255);")
        gui.Menu.setVisible(0)
        QTimer.singleShot(2000, lambda:
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

    # \/ v30.11.24.2
    def send_left_command(self):
        response = self.communicator.send_left_command()
        print(f"[INFO]: {response}")

    def send_right_command(self):
        response = self.communicator.send_right_command()
        print(f"[INFO]: {response}")

    def connect(self):
        response = self.communicator.connect()
        print(f"[INFO]: {response}")
    # /\ v30.11.24.2