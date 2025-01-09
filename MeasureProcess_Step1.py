from PySide6.QtCore import QTimer

from FC500Com import FC500Com
from ESPCom import ESPCom #changed SerialCommunicator to ESPCom
from LoggingHandler import Logger
from gui_ui import Ui_Main
from settings import Settings
from Measure_Lights import Measure_Lights
from MeasureProcess_Step2 import MeasureProcess_Steps2

fc500_override = False
esp_override = False

class MeasureProcess_Steps1:
    def __init__(self, gui:Ui_Main, settings:Settings):
        self.logger = Logger()
        self.gui = gui
        self.Step_Light = Measure_Lights()
        self.measure2 = MeasureProcess_Steps2(gui, settings)

        try:
            self.FC500 = FC500Com(settings)
        except Exception as e:
            self.logger.log_error(f"Start Up: Nie można połączyć się z FC500. Proszę sprawdzić kabel oraz stan urządzenia. Odłączenie i ponowne podłączenie kabla może być wymagane. Błąd: {e}")
        try:
            self.ESP = ESPCom(settings)
        except Exception as e:
            self.logger.log_error(f"Start Up: Nie można połączyć się z mikrokontrolerem ESP. Proszę sprawdzić kabel oraz stan urządzenia. Odłączenie i ponowne podłączenie kabla może być wymagane. Błąd: {e}")

    def begin(self):
        self.logger.log_info("Measure Process: Step 1")
        self.gui.btn_Measure_Step1_ObjectReady.setEnabled(False)
        self.Step_Light.Set_Processing(1, self.gui.LightIndicatorContainer.parentWidget(), toggle=True)
        self.gui.SubScreens_Measure.setCurrentWidget(self.gui.SubScreen_Measure_Step1)
        QTimer.singleShot(1700, lambda:(self.Measure_Step1_1()))

    def Measure_Step1_1(self):
        fc500_connected = False
        esp_connected = False

        self.fc500_override = True
        self.esp_override = True

        try:
            if self.FC500.connection_check() or self.fc500_override == True:
                self.logger.log_info("Measure: Połączenie nawiązane z FC500")
                self.Step_Light.Set_True("1_1", self.gui.dsp_MeasureProgress_Step_1_1.parentWidget())
                fc500_connected = True
            else:
                self.logger.log_error("Measure: Brak połączenia z FC500")
        except Exception as e:
            self.logger.log_error(f"Measure: Błąd podczas sprawdzania połączenia z FC500: {e}")
        try:
            status, message = self.ESP.connect()
            if status or self.esp_override == True:
                self.logger.log_info("Measure: Połączenie nawiązane z mikrokontrolerem ESP")
                self.Step_Light.Set_True("1_2", self.gui.dsp_MeasureProgress_Step_1_2.parentWidget())
                esp_connected = True
            else:
                self.logger.log_error(f"Measure: Brak połączenia z ESP - {message}")
        except Exception as e:
            self.logger.log_error(f"Measure: Błąd podczas sprawdzania połączenia z ESP: {e}")

        if fc500_connected and esp_connected or self.fc500_override and self.esp_override:
            self.logger.log_info("Measure: Oba urządzenia są podłączone, kontynuowanie procesu")
            #self.safety_unlock()
            self.Step_Light.Set_Processing(1, self.gui.dsp_MeasureProgress_Step_1.parentWidget(), toggle=False)
            self.Step_Light.Set_Processing_True(1, self.gui.dsp_MeasureProgress_Step_1.parentWidget(), toggle=True)
            self.gui.btn_Measure_Step1_ObjectReady.setEnabled(True)
        else:
            # Zarządzanie błędami
            if not fc500_connected and not esp_connected and not self.fc500_override and not self.esp_override:
                self.logger.log_error("Measure: Brak połączenia z FC500 oraz ESP")
                self.Measure_Step1_ErrorFC()
                self.Measure_Step1_ErrorESP()
            elif not fc500_connected and not self.fc500_override:
                self.Measure_Step1_ErrorFC()
            elif not esp_connected and not self.esp_override:
                self.Measure_Step1_ErrorESP()



    def Measure_Step1_ErrorFC(self):
        self.logger.log_error("Measure: Nie można połączyć się z FC500. Proszę sprawdzić kabel oraz stan urządzenia. Odłączenie i ponowne podłączenie kabla lub/oraz restart programu mogą być wymagane.")
        self.Step_Light.Set_Processing(1, self.gui.LightIndicatorContainer.parentWidget(), toggle=False)
        self.Step_Light.Set_Processing_False(1, self.gui.LightIndicatorContainer.parentWidget(), toggle=True)
        self.Step_Light.Set_False("1_1", self.gui.dsp_MeasureProgress_Step_1_1.parentWidget())
        if self.gui.SubScreens_Measure.currentWidget() != self.gui.SubScreen_Measure_Step1_Error:
            self.gui.SubScreens_Measure.setCurrentWidget(self.gui.SubScreen_Measure_Step1_Error)
    


    def Measure_Step1_ErrorESP(self):
        self.logger.log_error("Measure: Nie można połączyć się z mikrokontrolerem ESP. Proszę sprawdzić stan podłączenia przewodów. Odłączenie i ponowne podłączenie kabla lub/oraz restart programu mogą być wymagane.") #TMQ Tu jakiś error pasujący do ESP
        self.Step_Light.Set_Processing(1, self.gui.LightIndicatorContainer.parentWidget(), toggle=False)
        self.Step_Light.Set_Processing_False(1, self.gui.LightIndicatorContainer.parentWidget(), toggle=True)
        self.Step_Light.Set_False("1_2", self.gui.dsp_MeasureProgress_Step_1_2.parentWidget())
        if self.gui.SubScreens_Measure.currentWidget() != self.gui.SubScreen_Measure_Step1_Error:
            self.gui.SubScreens_Measure.setCurrentWidget(self.gui.SubScreen_Measure_Step1_Error)
    


    def Measure_Step1_Error_Refresh(self):
        try:
            self.FC500.connection_incoming()
            self.ESPCom.send_left_command()
            try:
                #TMQ taki sam connection check jak wyżej w Measure_Step1
                self.Measure_Step1_1()
            except:
                self.logger.log_error("ESP") #TMQ Tu jakiś error pasujący do ESP
        except:
            self.logger.log_error("Measure: Nie można połączyć się z FC500. Proszę sprawdzić kabel oraz stan urządzenia. Odłączenie i ponowne podłączenie kabla lub/oraz restart programu mogą być wymagane.")