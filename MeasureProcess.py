from PySide6.QtCore import QTimer

from FC500Com import FC500Com
from LoggingHandler import Logger
from gui_ui import Ui_Main
from Measure_Lights import Measure_Lights
from settings import Settings
from ESPCom import ESPCom #changed SerialCommunicator to ESPCom
from GraphLimits import ForceChecker

from MeasureProcess_Step1 import MeasureProcess_Steps1
from MeasureProcess_Step2 import MeasureProcess_Steps2


class MeasureProcess:
    
    def __init__(self, gui:Ui_Main, settings:Settings):
        self.logger = Logger()
        self.gui = gui
        self.measure1 = MeasureProcess_Steps1(gui, settings)
        self.measure2 = MeasureProcess_Steps2(gui, settings)
        self.Step_Light = Measure_Lights()
        self.settings = settings
        self.Step_Flags = 0

    def StopCycle(self):
        self.MainCycle.cancel()
        self.CycleCleanUp()
        self.logger.log_warning("Measure process aborted!")

    def CycleCleanUp(self):
        self.gui.SubScreens_Measure.setCurrentWidget(self.gui.SubScreen_Measure_Step1)
        self.gui.btn_Measure_Step2_LockSafety.setEnabled(True)
        self.Step_Light.Set_Empty("1_1", self.gui.dsp_MeasureProgress_Step_1_1.parentWidget())
        self.Step_Light.Set_Empty("2_1", self.gui.dsp_MeasureProgress_Step_2_1.parentWidget())
        self.Step_Light.Set_Processing("2_1", self.gui.dsp_MeasureProgress_Step_2_1.parentWidget(), toggle=False)
        self.Step_Light.Set_Empty("2_1", self.gui.dsp_MeasureProgress_Step_1_1.parentWidget())

        parent_widget = self.gui.LightIndicatorContainer.parentWidget()
        toggle = False

        for i in range(1, 5):
            self.Step_Light.Set_Processing(i, parent_widget, toggle)
            self.Step_Light.Set_Processing_True(i, parent_widget, toggle)
            self.Step_Light.Set_Processing_False(i, parent_widget, toggle)
            self.Step_Light.Set_Empty(i, parent_widget)

    def MeasureCycle(self):
        try:
            if self.gui.SubScreens_Measure.currentWidget() == self.gui.SubScreen_Measure_Step1 and self.Step_Flags == 0:
                self.Step_Flags = 1
                self.measure1.begin()
            elif self.gui.SubScreens_Measure.currentWidget() == self.gui.SubScreen_Measure_Step2 and self.Step_Flags == 1:
                self.Step_Flags = 2
                self.measure2.begin()
        except Exception as e:
            self.logger.log_error(f"An error occured inside of MeasureCycle: {e}")


    async def Measure_Step1(self):
        self.logger.log_info("Measure Process: Step 1")
        self.gui.btn_Measure_Step1_ObjectReady.setEnabled(False)
        self.Step_Light.Set_Processing(1, self.gui.LightIndicatorContainer.parentWidget(), toggle=True)
        self.gui.SubScreens_Measure.setCurrentWidget(self.gui.SubScreen_Measure_Step1)

        fc500_connected = False
        esp_connected = False
        # fc500_connected = True
        # esp_connected = True

        # Sprawdzenie połączenia z FC500
        try:
            if self.FC500.connection_check():
                self.logger.log_info("Measure: Połączenie nawiązane z FC500")
                self.Step_Light.Set_True("1_1", self.gui.dsp_MeasureProgress_Step_1_1.parentWidget())
                fc500_connected = True
            else:
                self.logger.log_error("Measure: Brak połączenia z FC500")
        except Exception as e:
            self.logger.log_error(f"Measure: Błąd podczas sprawdzania połączenia z FC500: {e}")

        # Sprawdzenie połączenia z ESP
        try:
            status, message = self.ESP.connect()
            if status:
                self.logger.log_info("Measure: Połączenie nawiązane z mikrokontrolerem ESP")
                self.Step_Light.Set_True("1_2", self.gui.dsp_MeasureProgress_Step_1_2.parentWidget())
                esp_connected = True
            else:
                self.logger.log_error(f"Measure: Brak połączenia z ESP - {message}")
        except Exception as e:
            self.logger.log_error(f"Measure: Błąd podczas sprawdzania połączenia z ESP: {e}")

        # Logika warunków
        if fc500_connected and esp_connected:
            self.logger.log_info("Measure: Oba urządzenia są podłączone, kontynuowanie procesu")
            await self.safety_unlock()
            self.Step_Light.Set_Processing(1, self.gui.dsp_MeasureProgress_Step_1.parentWidget(), toggle=False)
            self.Step_Light.Set_Processing_True(1, self.gui.dsp_MeasureProgress_Step_1.parentWidget(), toggle=True)
            self.gui.btn_Measure_Step1_ObjectReady.setEnabled(True)
            await self.MeasureCycle()
        else:
            # Zarządzanie błędami
            if not fc500_connected and not esp_connected:
                self.logger.log_error("Measure: Brak połączenia z FC500 oraz ESP")
                self.Measure_Step1_ErrorFC()
                self.Measure_Step1_ErrorESP()
            elif not fc500_connected:
                self.Measure_Step1_ErrorFC()
            elif not esp_connected:
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
    
    async def Measure_Step1_Error_Refresh(self):
        try:
            self.FC500.connection_check()
            self.ESPCom.send_left_command()
            try:
                #TMQ taki sam connection check jak wyżej w Measure_Step1
                self.Measure_Step1()
            except:
                self.logger.log_error("ESP") #TMQ Tu jakiś error pasujący do ESP
        except:
            self.logger.log_error("Measure: Nie można połączyć się z FC500. Proszę sprawdzić kabel oraz stan urządzenia. Odłączenie i ponowne podłączenie kabla lub/oraz restart programu mogą być wymagane.")

    async def safety_unlock(self):
        pass

    async def safety_lock(self):
        pass

    async def Measure_Step2(self):
        self.logger.log_info("Measure Process: Step 2")
        self.Step_Light.Set_Processing_True(1, self.gui.dsp_MeasureProgress_Step_1.parentWidget(), toggle=False)
        self.Step_Light.Set_True(1, self.gui.LightIndicatorContainer.parentWidget())
        self.Step_Light.Set_Processing(2, self.gui.dsp_MeasureProgress_Step_1.parentWidget(), toggle=True)
        
        
      
    