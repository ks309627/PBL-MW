from gui_ui import Ui_Main
from PySide6.QtCore import QTimer
# v30.11.24.2
from EspCom import SerialCommunicator

class ScreenControler:
    def __init__(self, gui:Ui_Main, communicator): #
            #Screen switch buttons
        gui.btn_Measure.clicked.connect(lambda: gui.Screen.setCurrentWidget(gui.Screen_MeasureMain))
        gui.btn_Graphs.clicked.connect(lambda: gui.Screen.setCurrentWidget(gui.Screen_Graphs))
        gui.btn_Settings.clicked.connect(lambda: gui.Screen.setCurrentWidget(gui.Screen_Settings))
        gui.btn_Errors.clicked.connect(lambda: gui.Screen.setCurrentWidget(gui.Screen_Errors))
        
        gui.btn_MeasureToGraph.clicked.connect(lambda: (gui.Screen.setCurrentWidget(gui.Screen_Graphs), self.ScreenSwitch_CategoryGraphs(gui)))
        gui.btn_StartMeasure.clicked.connect(lambda: (gui.Screen.setCurrentWidget(gui.Screen_MeasureProgress), self.ScreenSwitch_CategoryMeasure(gui)))
        gui.btn_StopMeasure.clicked.connect(lambda: (gui.Screen.setCurrentWidget(gui.Screen_MeasureMain), self.ScreenSwitch_CategoryMeasure(gui)))

        # v30.11.24.2 - added comunicator v30.11.24.2
        self.gui = gui
        self.communicator = communicator
        gui.pushButton.clicked.connect(self.send_left_command)
        gui.pushButton_2.clicked.connect(self.send_right_command)
        gui.pushButton_3.clicked.connect(self.connect)

        self.graphControler = None
        gui.btn_Graph_left.clicked.connect(self.move_graph_left)
        gui.btn_Graph_right.clicked.connect(self.move_graph_right)
        gui.btn_Graph_up.clicked.connect(self.move_graph_up)
        gui.btn_Graph_down.clicked.connect(self.move_graph_down)
        gui.btn_Graph_zin.clicked.connect(self.zoom_graph_in)
        gui.btn_Graph_zout.clicked.connect(self.zoom_graph_out)
        gui.btn_Graph_resetview.clicked.connect(self.view_graph_reset)

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