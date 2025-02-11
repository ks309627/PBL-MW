from gui_ui import Ui_Main
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QCheckBox, QFileDialog, QMessageBox, QDialog, QPushButton
from settings import Settings
from LoginDialog import LoginDialog

from FC500Com import FC500Com
from ESPCom import ESPCom
#from MeasureProcess import MeasureProcess

from GraphList import GraphList
from GraphControler import GraphControler

from TerminalControler import TerminalControler
from LoggingHandler import Logger

#from MeasureProcess_Step1 import MeasureProcess_Steps1
#from MeasureProcess_Step2 import MeasureProcess_Steps2
from MeasureProcess_v2 import MeasureProcess
from Measure_Lights import Measure_Lights



class ScreenControler:
    def __init__(self, gui:Ui_Main, settings:Settings, measure_process:MeasureProcess):

        self.gui = gui
        #self.communicator = communicator
        self.settings = settings
        self.graphList = GraphList(gui, settings)
        self.graphControler = GraphControler(gui, settings)
        self.measure_process = measure_process

        #self.measure1 = MeasureProcess_Steps1(gui, settings)
        #self.measure2 = MeasureProcess_Steps2(gui, settings)

        self.Step_Light = Measure_Lights()

        self.logger = Logger()
        self.measureProcess = MeasureProcess(gui, settings)
        self.FC500 = FC500Com(settings)
        self.ESP = ESPCom(settings)

        self.graph_mode = 0
        self.graph_relative_mode = 0


        gui.btn_Measure.clicked.connect(lambda: gui.Screen.setCurrentWidget(gui.Screen_MeasureMain))
        gui.btn_Graphs.clicked.connect(lambda: (gui.Screen.setCurrentWidget(gui.Screen_Graphs), self.graphUpdate()))
        gui.btn_Settings.clicked.connect(lambda: gui.Screen.setCurrentWidget(gui.Screen_Settings))
        gui.btn_Errors.clicked.connect(lambda: (gui.Screen.setCurrentWidget(gui.Screen_Errors), self.logger._clean_up_old_logs(), self.terminalControler.Perform_Refresh()))
        
        gui.btn_MeasureToGraph.clicked.connect(lambda: (gui.Screen.setCurrentWidget(gui.Screen_Graphs), self.ScreenSwitch_CategoryGraphs(gui)))
        #
        gui.btn_StartMeasure.clicked.connect(lambda: (gui.Screen.setCurrentWidget(gui.Screen_MeasureProgress), self.ScreenSwitch_CategoryMeasure(gui), self.BeginMeasure()))
        #gui.btn_StartMeasure.clicked.connect(lambda: (gui.Screen.setCurrentWidget(gui.Screen_MeasureProgress), self.ScreenSwitch_CategoryMeasure(gui), self.BeginMeasure()))
        
        
        gui.btn_StopMeasure.clicked.connect(lambda: (gui.Screen.setCurrentWidget(gui.Screen_MeasureMain), self.ScreenSwitch_CategoryMeasure(gui), self.StopMeasure_Safety()))

        gui.btn_Measure_Step1_ObjectReady.clicked.connect(lambda:(gui.SubScreens_Measure.setCurrentWidget(gui.SubScreen_Measure_Step2), self.gotoStep2()))

        gui.btn_Measure_Step1_Error_Errors.clicked.connect(lambda:(self.StopMeasure(), gui.Screen.setCurrentWidget(gui.Screen_Errors), self.ScreenSwitch_CategoryErrors(gui), self.logger._clean_up_old_logs(), self.terminalControler.Perform_Refresh()))
        gui.btn_Measure_Step1_Error_RefreshCOM.clicked.connect(lambda:(self.MeasureComRefresh()))

        gui.btn_Measure_Step2_LockSafety.clicked.connect(lambda:(gui.SubScreens_Measure.setCurrentWidget(gui.SubScreen_Measure_Step3), self.gotoStep3()))
        gui.btn_Measure_Step3.clicked.connect(lambda:(gui.SubScreens_Measure.setCurrentWidget(gui.SubScreen_Measure_Step4), self.gotoStep4()))
        

        # v30.11.24.2 - added comunicator v30.11.24.2
        self.gui = gui
        #self.communicator = communicator
        # gui.pushButton.clicked.connect(self.send_left_command)
        # gui.pushButton_2.clicked.connect(self.send_right_command)
        # gui.pushButton_3.clicked.connect(self.connect)

        gui.btn_Graph_left.clicked.connect(self.move_graph_left)
        gui.btn_Graph_right.clicked.connect(self.move_graph_right)
        gui.btn_Graph_up.clicked.connect(self.move_graph_up)
        gui.btn_Graph_down.clicked.connect(self.move_graph_down)
        gui.btn_Graph_zin.clicked.connect(self.zoom_graph_in)
        gui.btn_Graph_zout.clicked.connect(self.zoom_graph_out)

        gui.btn_Graph_refresh.clicked.connect(self.graph_refresh)
        gui.btn_Graph_resetview.clicked.connect(self.view_graph_reset)

        gui.btn_SaveGraph.clicked.connect(self.handle_save_graph)
        gui.btn_LoadGraph.clicked.connect(self.handle_load_graph)
        gui.btn_DeleteGraph.toggled.connect(self.handle_delete)

        gui.btn_Graph_mode.clicked.connect(self.change_graph_mode)
        gui.btn_Graph_relative.clicked.connect(self.change_graph_relative_mode)
        self.gui.btn_Graph_relative.setEnabled(False)

        gui.devMode.clicked.connect(self.handle_dev_mode)

        self.graphSavePath = gui.graphSavePath
        self.graphSavePath.setText(self.settings.get("graphSavePath"))

        self.COMPathFC = gui.COMPathFC
        self.COMPathFC.setText(self.settings.get("COMPathFC"))

        self.COMPathESP = gui.COMPathESP
        self.COMPathESP.setText(self.settings.get("COMPathESP"))

        gui.btn_settingsDefault.clicked.connect(self.restore_settings)
        gui.btn_settingsSave.clicked.connect(self.save_settings_to_file)

        self.terminalControler = TerminalControler(gui, settings)
        gui.btn_Errors_AllHistory_basic.clicked.connect(self.ButtonSwitch_Errors_AllH_basic)
        gui.btn_Errors_InstanceHistory_basic.clicked.connect(self.ButtonSwitch_Errors_InsH_basic)
        gui.btn_Errors_AllHistory_admin.clicked.connect(self.ButtonSwitch_Errors_AllH_admin)
        gui.btn_Errors_InstanceHistory_admin.clicked.connect(self.ButtonSwitch_Errors_InsH_admin)
        gui.btn_Errors_Refresh_basic.clicked.connect(self.Errors_Refresh_Loop)
        gui.btn_Errors_Refresh_admin.clicked.connect(self.Errors_Refresh_Loop)

        gui.btn_Errors_Send_admin.clicked.connect(self.Errors_Command)

        self.gui.btn_Measure_Step2_Right1.clicked.connect(lambda: self.measure_process.send_esp_command_r1())
        self.gui.btn_Measure_Step2_Right2.clicked.connect(lambda: self.measure_process.send_esp_command_r2())
        self.gui.btn_Measure_Step2_Right3.clicked.connect(lambda: self.measure_process.send_esp_command_r3())

        self.gui.btn_Measure_Step2_Left1.clicked.connect(lambda: self.measure_process.send_esp_command_l1())
        self.gui.btn_Measure_Step2_Left2.clicked.connect(lambda: self.measure_process.send_esp_command_l2())
        self.gui.btn_Measure_Step2_Left3.clicked.connect(lambda: self.measure_process.send_esp_command_l3())

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
            self.measureProcess.Step_Flags = 0
            self.gui.SubScreens_Measure.setCurrentWidget(self.gui.SubScreen_Measure_Step1) 
            #self.measureProcess.MeasureCycle()
            self.measureProcess.begin()
            self.gui.btn_Measure.setEnabled(False)
            self.gui.btn_Graphs.setEnabled(False)
            self.gui.btn_Settings.setEnabled(False)
            self.gui.btn_Errors.setEnabled(False)

    def gotoStep2(self):
        if self.measureProcess:
            self.measureProcess.Step2()
    
    def MeasureComRefresh(self):
        if self.measureProcess:
            # self.ESP.close()
            # self.Step_Light.Set_Empty("1_1", self.gui.dsp_MeasureProgress_Step_1_2.parentWidget())
            # self.Step_Light.Set_Empty("1_2", self.gui.dsp_MeasureProgress_Step_1_2.parentWidget())
            # #self.measureProcess.check_devices()
            # #QTimer.singleShot(1700, lambda:(self.measureProcess.Step1()))
            # QTimer.singleShot(1700, lambda:(self.measureProcess.check_devices()))
            self.measureProcess.Refresh()


    def StopMeasure(self):
        if self.measureProcess:
            self.measureProcess.StopCycle()
            
            self.gui.btn_Measure.setEnabled(True)
            self.gui.btn_Graphs.setEnabled(True)
            self.gui.btn_Settings.setEnabled(True)
            self.gui.btn_Errors.setEnabled(True)
    
    def StopMeasure_Safety(self):
        if self.measureProcess:
            self.logger.log_warning("Safety Mushroom Pressed!")
            self.StopMeasure()

    def gotoStep3(self):
        if self.measureProcess:
            self.measureProcess.Step3()

    def gotoStep4(self):
        if self.measureProcess:
            self.measureProcess.Step4()




#   to jest do usunięcia, ale można jeszcze zostawić w razie czego

    # def send_left_command(self):
    #     response = self.communicator.send_left_command()
    #     print(f"[INFO]: {response}")

    # def send_right_command(self):
    #     response = self.communicator.send_right_command()
    #     print(f"[INFO]: {response}")

    # def connect(self):
    #     self.settings.load_settings()
    #     new_port = self.settings.get("COMPathESP")

    #     if new_port:
    #         self.communicator.update_com_path(new_port)
    #         response = self.communicator.connect()
    #         print(f"[INFO]: {response}")
    #     else:
    #         print("[ERROR]: Nie znaleziono klucza 'COMPathESP' w ustawieniach.")
            
    def graphUpdate(self):
        self.graphList.refresh_graph
        self.graphList.refresh()


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

    def graph_refresh(self):
        if self.graphControler:
            self.graphList.refresh()

    def view_graph_reset(self):
        if self.graphControler:
            self.graphControler.reset()

    def restore_settings(self):
        self.settings.reset_to_defaults()
        self.gui.devMode.setChecked(bool(self.settings.get("devMode")))
        self.graphSavePath.setText(self.settings.get("graphSavePath"))
        self.COMPathFC.setText(self.settings.get("COMPathFC"))
        self.COMPathESP.setText(self.settings.get("COMPathESP"))

    def save_settings_to_file(self):
        self.settings.set("devMode", int(self.gui.devMode.isChecked()))
        self.settings.set("graphSavePath", self.graphSavePath.text())
        self.settings.set("COMPathFC", self.COMPathFC.text())
        self.settings.set("COMPathESP", self.COMPathESP.text())
        self.settings.save_settings()
    
    def set_graph_controler(self, graphControler):
        self.graphControler = graphControler

    def handle_save_graph(self):
        if self.graphControler:
            self.graphList.save_graph_to_file()

    def handle_load_graph(self):
        if self.graphControler:
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getOpenFileName(None, "Wczytaj wykres", "", "JSON Files (*.json)")
            if file_path:
                self.graphList.load_graph_from_file(file_path)

    def handle_delete(self, checked):
        if self.graphControler:
            if checked:
                self.graphList.deleteMode_on()
            else:
                self.graphList.deleteMode_off()

    # v30.12.24.1 - added test button to check if it connects with FC500 - needs further testing
    # def fc500_zero(self):
    #     if self.fc500:
    #         self.fc500.cmd_zero()

    def handle_dev_mode(self):
        if self.gui.devMode.isChecked():
            login_dialog = LoginDialog()
            if login_dialog.exec() == QDialog.Accepted:
                self.settings.set("devMode", 1)
                self.logger.log_info("DevMode został włączony.")
                self.settings.save_settings()
            else:
                self.gui.devMode.setChecked(False)
                self.logger.log_info("DevMode nie został włączony - brak autoryzacji.")
        else:
            if self.settings.get("devMode") == 1:
                self.settings.set("devMode", 0)
                self.logger.log_info("DevMode został wyłączony.")
                self.settings.save_settings()

    def ButtonSwitch_Errors_AllH_basic(self):
        if self.terminalControler:
            self.terminalControler.read_log_file(self.terminalControler.text_edit_basic, 'logs/JoinedLogs.log')
        self.gui.btn_Errors_AllHistory_basic.setChecked(1)
        self.gui.btn_Errors_InstanceHistory_basic.setChecked(0)

    def ButtonSwitch_Errors_InsH_basic(self):
        if self.terminalControler:
            self.terminalControler.read_log_file(self.terminalControler.text_edit_basic)
        self.gui.btn_Errors_AllHistory_basic.setChecked(0)
        self.gui.btn_Errors_InstanceHistory_basic.setChecked(1)

    def ButtonSwitch_Errors_AllH_admin(self):
        if self.terminalControler:
            self.terminalControler.read_log_file(self.terminalControler.text_edit_admin, 'logs/JoinedLogs.log')
        self.gui.btn_Errors_AllHistory_admin.setChecked(1)
        self.gui.btn_Errors_InstanceHistory_admin.setChecked(0)

    def ButtonSwitch_Errors_InsH_admin(self):
        if self.terminalControler:
            self.terminalControler.read_log_file(self.terminalControler.text_edit_admin)
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



    def change_graph_mode(self):
        self.graph_mode = 1 - self.graph_mode  # Przełączanie między 0 i 1
        
        if self.graph_mode == 1:
            print("step mode")
            self.gui.btn_Graph_relative.setEnabled(True)
        else:
            print("time mode")
            self.gui.btn_Graph_relative.setEnabled(False)

    def change_graph_relative_mode(self):
        self.graph_relative_mode = 1 - self.graph_relative_mode # Przełączanie między 0 i 1
        
        if self.graph_relative_mode == 1:
            print("relative mode on")
        else:
            print("relative mode off")
