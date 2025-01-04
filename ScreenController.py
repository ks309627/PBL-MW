from gui_ui import Ui_Main
from PySide6.QtCore import QTimer
# v30.11.24.2
from EspCom import SerialCommunicator
from FC500Com import FC500Com

from MeasureProcess import MeasureProcess
import asyncio

from TerminalControler import TerminalControler
from LoggingHandler import ErrorLogger


class ScreenControler:
    def __init__(self, gui:Ui_Main, communicator): #
        
        self.logger = ErrorLogger()
        self.measureProcess = MeasureProcess()
        
            #Screen switch buttons
        gui.btn_Measure.clicked.connect(lambda: gui.Screen.setCurrentWidget(gui.Screen_MeasureMain))
        gui.btn_Graphs.clicked.connect(lambda: gui.Screen.setCurrentWidget(gui.Screen_Graphs))
        gui.btn_Settings.clicked.connect(lambda: gui.Screen.setCurrentWidget(gui.Screen_Settings))
        gui.btn_Errors.clicked.connect(lambda: (gui.Screen.setCurrentWidget(gui.Screen_Errors), self.logger._clean_up_old_logs(), self.terminalControler.Perform_Refresh()))
        
        gui.btn_MeasureToGraph.clicked.connect(lambda: (gui.Screen.setCurrentWidget(gui.Screen_Graphs), self.ScreenSwitch_CategoryGraphs(gui)))
        gui.btn_StartMeasure.clicked.connect(lambda: (gui.Screen.setCurrentWidget(gui.Screen_MeasureProgress), self.ScreenSwitch_CategoryMeasure(gui), self.BeginMeasure()))
        gui.btn_StopMeasure.clicked.connect(lambda: (gui.Screen.setCurrentWidget(gui.Screen_MeasureMain), self.ScreenSwitch_CategoryMeasure(gui), self.StopMeasure()))


        # v30.11.24.2 - added comunicator v30.11.24.2
        self.gui = gui
        self.communicator = communicator
        # gui.pushButton.clicked.connect(self.send_left_command)
        # gui.pushButton_2.clicked.connect(self.send_right_command)
        # gui.pushButton_3.clicked.connect(self.connect)

        self.graphControler = None
        gui.btn_Graph_left.clicked.connect(self.move_graph_left)
        gui.btn_Graph_right.clicked.connect(self.move_graph_right)
        gui.btn_Graph_up.clicked.connect(self.move_graph_up)
        gui.btn_Graph_down.clicked.connect(self.move_graph_down)
        gui.btn_Graph_zin.clicked.connect(self.zoom_graph_in)
        gui.btn_Graph_zout.clicked.connect(self.zoom_graph_out)
        gui.btn_Graph_resetview.clicked.connect(self.view_graph_reset)

        # v30.12.24.1 - added test button to check if it connects with FC500 - needs further testing
        #self.fc500 = None
        #gui.btn_FC500Com_cmd_zero.clicked.connect(self.fc500_zero)

        self.terminalControler = TerminalControler(gui)
        gui.btn_Errors_AllHistory_basic.clicked.connect(self.ButtonSwitch_Errors_AllH_basic)
        gui.btn_Errors_InstanceHistory_basic.clicked.connect(self.ButtonSwitch_Errors_InsH_basic)
        gui.btn_Errors_AllHistory_admin.clicked.connect(self.ButtonSwitch_Errors_AllH_admin)
        gui.btn_Errors_InstanceHistory_admin.clicked.connect(self.ButtonSwitch_Errors_InsH_admin)
        gui.btn_Errors_Refresh_basic.clicked.connect(self.Errors_Refresh_Loop)
        gui.btn_Errors_Refresh_admin.clicked.connect(self.Errors_Refresh_Loop)

        gui.btn_Errors_Send_admin.clicked.connect(self.Errors_Command)


        #Additional Screen switch actions
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

    def BeginMeasure(self):
        if self.measureProcess:
            asyncio.run(self.measureProcess.MeasureCycle())
            self.gui.btn_Measure.setEnabled(False)
            self.gui.btn_Graphs.setEnabled(False)
            self.gui.btn_Settings.setEnabled(False)
            self.gui.btn_Errors.setEnabled(False)
    
    def StopMeasure(self):
        if self.measureProcess:
            self.measureProcess.StopCycle()
            self.gui.btn_Measure.setEnabled(True)
            self.gui.btn_Graphs.setEnabled(True)
            self.gui.btn_Settings.setEnabled(True)
            self.gui.btn_Errors.setEnabled(True)

    # v30.11.24.2
    def send_left_command(self):
        response = self.communicator.send_left_command()
        print(f"[INFO]: {response}")

    def send_right_command(self):
        response = self.communicator.send_right_command()
        print(f"[INFO]: {response}")

    def connect(self):
        response = self.communicator.connect()
        print(f"[INFO]: {response}")

    def set_graph_controler(self, graphControler):
        self.graphControler = graphControler

    def move_graph_left(self):
        if self.graphControler:
            self.graphControler.scroll_left()

    def move_graph_right(self):
        if self.graphControler:
            self.graphControler.scroll_right()

    def move_graph_up(self):
        if self.graphControler:
            self.graphControler.scroll_up()

    def move_graph_down(self):
        if self.graphControler:
            self.graphControler.scroll_down()

    def zoom_graph_in(self):
        if self.graphControler:
            self.graphControler.zoom_in()

    def zoom_graph_out(self):
        if self.graphControler:
            self.graphControler.zoom_out()

    def view_graph_reset(self):
        if self.graphControler:
            self.graphControler.reset()

    # v30.12.24.1 - added test button to check if it connects with FC500 - needs further testing
    # def fc500_zero(self):
    #     if self.fc500:
    #         self.fc500.cmd_zero()

    def ButtonSwitch_Errors_AllH_basic(self):
        if self.terminalControler:
            self.terminalControler.JoinedLogs_basic()
        self.gui.btn_Errors_AllHistory_basic.setChecked(1)
        self.gui.btn_Errors_InstanceHistory_basic.setChecked(0)

    def ButtonSwitch_Errors_InsH_basic(self):
        if self.terminalControler:
            self.terminalControler.SingleLog_basic()
        self.gui.btn_Errors_AllHistory_basic.setChecked(0)
        self.gui.btn_Errors_InstanceHistory_basic.setChecked(1)

    def ButtonSwitch_Errors_AllH_admin(self):
        if self.terminalControler:
            self.terminalControler.JoinedLogs_admin()
        self.gui.btn_Errors_AllHistory_admin.setChecked(1)
        self.gui.btn_Errors_InstanceHistory_admin.setChecked(0)

    def ButtonSwitch_Errors_InsH_admin(self):
        if self.terminalControler:
            self.terminalControler.SingleLog_admin()
        self.gui.btn_Errors_AllHistory_admin.setChecked(0)
        self.gui.btn_Errors_InstanceHistory_admin.setChecked(1)

    def Errors_Refresh_Loop(self):
        if self.terminalControler:
            self.terminalControler.Refresh_Loop()

    def Errors_Refresh(self):
        if self.terminalControler:
            self.terminalControler.Perform_Refresh()

    def Errors_Command(self):
        if self.terminalControler:
            self.terminalControler.Send_Command_admin()