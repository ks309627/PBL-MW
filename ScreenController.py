from gui_ui import Ui_Main
from PySide6.QtCore import QTimer
from EspCom import SerialCommunicator
from PySide6.QtWidgets import QCheckBox
from settings import Settings

class ScreenControler:
    def __init__(self, gui:Ui_Main, communicator, settings:Settings):

        self.gui = gui
        self.communicator = communicator
        self.graphControler = None
        self.settings = settings

        gui.btn_Measure.clicked.connect(lambda: gui.Screen.setCurrentWidget(gui.Screen_MeasureMain))
        gui.btn_Graphs.clicked.connect(lambda: gui.Screen.setCurrentWidget(gui.Screen_Graphs))
        gui.btn_Settings.clicked.connect(lambda: gui.Screen.setCurrentWidget(gui.Screen_Settings))
        gui.btn_Errors.clicked.connect(lambda: gui.Screen.setCurrentWidget(gui.Screen_Errors))
        
        gui.btn_MeasureToGraph.clicked.connect(lambda: (gui.Screen.setCurrentWidget(gui.Screen_Graphs), self.ScreenSwitch_CategoryGraphs(gui)))
        gui.btn_StartMeasure.clicked.connect(lambda: (gui.Screen.setCurrentWidget(gui.Screen_MeasureProgress), self.ScreenSwitch_CategoryMeasure(gui)))
        gui.btn_StopMeasure.clicked.connect(lambda: (gui.Screen.setCurrentWidget(gui.Screen_MeasureMain), self.ScreenSwitch_CategoryMeasure(gui)))

        gui.pushButton.clicked.connect(self.send_left_command)
        gui.pushButton_2.clicked.connect(self.send_right_command)
        gui.pushButton_3.clicked.connect(self.connect)

        gui.btn_Graph_left.clicked.connect(self.move_graph_left)
        gui.btn_Graph_right.clicked.connect(self.move_graph_right)
        gui.btn_Graph_up.clicked.connect(self.move_graph_up)
        gui.btn_Graph_down.clicked.connect(self.move_graph_down)
        gui.btn_Graph_zin.clicked.connect(self.zoom_graph_in)
        gui.btn_Graph_zout.clicked.connect(self.zoom_graph_out)
        gui.btn_Graph_resetview.clicked.connect(self.view_graph_reset)

        self.devMode = gui.devMode
        self.devMode.setChecked(bool(self.settings.get("devMode")))

        self.graphSavePath = gui.graphSavePath
        self.graphSavePath.setText(self.settings.get("graphSavePath"))

        self.COMPath = gui.COMPath
        self.COMPath.setText(self.settings.get("COMPath"))

        self.COMPathESP = gui.COMPathESP
        self.COMPathESP.setText(self.settings.get("COMPathESP"))

        gui.btn_settingsDefault.clicked.connect(self.restore_settings)
        gui.btn_settingsSave.clicked.connect(self.save_settings_to_file)

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

    def send_left_command(self):
        response = self.communicator.send_left_command()
        print(f"[INFO]: {response}")

    def send_right_command(self):
        response = self.communicator.send_right_command()
        print(f"[INFO]: {response}")

    #\/    v02.01.25.1
    def connect(self):
        self.settings.load_settings()
        new_port = self.settings.get("COMPathESP")

        if new_port:
            self.communicator.update_com_path(new_port)
            response = self.communicator.connect()
            print(f"[INFO]: {response}")
        else:
            print("[ERROR]: Nie znaleziono klucza 'COMPathESP' w ustawieniach.")
    #/\
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

    #\/    v02.01.25.1
    def restore_settings(self):
        self.settings.reset_to_defaults()
        self.devMode.setChecked(bool(self.settings.get("devMode")))
        self.graphSavePath.setText(self.settings.get("graphSavePath"))
        self.COMPath.setText(self.settings.get("COMPath"))
        self.COMPathESP.setText(self.settings.get("COMPathESP"))

    def save_settings_to_file(self):
        self.settings.set("devMode", int(self.devMode.isChecked()))
        self.settings.set("graphSavePath", self.graphSavePath.text())
        self.settings.set("COMPath", self.COMPath.text())
        self.settings.set("COMPathESP", self.COMPathESP.text())
        self.settings.save_settings()
    #/\