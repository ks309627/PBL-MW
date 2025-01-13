from PySide6.QtCore import QTimer
from gui_ui import Ui_Main
from FC500Com import FC500Com
from ESPCom import ESPCom
from LoggingHandler import Logger
from Measure_Lights import Measure_Lights
from settings import Settings
from GraphLimits import ForceChecker

class MeasureProcess:
    def __init__(self, gui:Ui_Main, settings:Settings):
        self.settings = settings
        self.gui = gui
        self.logger = Logger()
        self.Step_Light = Measure_Lights()
        
        self.ESP = None
        self.FC500 = None
        self.Step_Flags = 0

        self.fc500_connected = False
        self.esp_connected = False


        self.init_devices()

    def init_devices(self):
        try:
            self.FC500 = FC500Com(self.settings)
            self.logger.log_info(f"Start Up: Pomyślnie połączono z siłomierzem FC500")
        except Exception as e:
            self.logger.log_error(f"Start Up: Nie można połączyć się z FC500. Proszę sprawdzić kabel oraz stan urządzenia. Odłączenie i ponowne podłączenie kabla może być wymagane. Błąd: {e}")
        try:
            self.ESP = ESPCom(self.settings)
            self.logger.log_info(f"Start Up: Pomyślnie połączono z mikrokontrolerem ESP")
        except Exception as e:
            self.logger.log_error(f"Start Up: Nie można połączyć się z mikrokontrolerem ESP. Proszę sprawdzić kabel oraz stan urządzenia. Odłączenie i ponowne podłączenie kabla może być wymagane. Błąd: {e}")

    def begin(self):
        self.logger.log_info("Measure Process: Begin")
        self.step_flags = 0
        self.gui.btn_Measure_Step1_ObjectReady.setEnabled(False)
        self.Step_Light.Set_Processing(1, self.gui.LightIndicatorContainer.parentWidget(), toggle=True)
        self.gui.SubScreens_Measure.setCurrentWidget(self.gui.SubScreen_Measure_Step1)
        QTimer.singleShot(1700, lambda:(self.Step1()))

    def Step1(self):
        self.init_devices()
        self.logger.log_info("Measure Process: Step1")
        self.check_devices()

        if self.fc500_connected and self.esp_connected:
            self.logger.log_info("Measure: Oba urządzenia są podłączone, przejście do Kroku 2")
            self.Step_Light.Set_Processing(1, self.gui.dsp_MeasureProgress_Step_1.parentWidget(), toggle=False)
            self.Step_Light.Set_Processing_True(1, self.gui.dsp_MeasureProgress_Step_1.parentWidget(), toggle=True)
            self.gui.btn_Measure_Step1_ObjectReady.setEnabled(True)
            self.Step2()
        if not self.fc500_connected:
            # if self.esp_connected:
            #     self.Step_Light.Set_True("1_2", self.gui.dsp_MeasureProgress_Step_1_2.parentWidget())
            self.logger.log_error("Measure: Nie można połączyć się z FC500. Proszę sprawdzić kabel oraz stan urządzenia. Odłączenie i ponowne podłączenie kabla lub/oraz restart programu mogą być wymagane.")
            self.Step_Light.Set_False("1_1", self.gui.dsp_MeasureProgress_Step_1_1.parentWidget())
            self.Step_Light.Set_Processing(1, self.gui.LightIndicatorContainer.parentWidget(), toggle=False)
            self.Step_Light.Set_Processing_False(1, self.gui.LightIndicatorContainer.parentWidget(), toggle=True)
            self.gui.SubScreens_Measure.setCurrentWidget(self.gui.SubScreen_Measure_Step1_Error)          
        if not self.esp_connected:
            # if self.fc500_connected:
            #     self.Step_Light.Set_True("1_1", self.gui.dsp_MeasureProgress_Step_1_2.parentWidget())
            self.logger.log_error("Measure: Nie można połączyć się z mikrokontrolerem ESP. Proszę sprawdzić stan podłączenia przewodów. Odłączenie i ponowne podłączenie kabla lub/oraz restart programu mogą być wymagane.") #TMQ Tu jakiś error pasujący do ESP
            self.Step_Light.Set_False("1_2", self.gui.dsp_MeasureProgress_Step_1_2.parentWidget())
            self.Step_Light.Set_Processing(1, self.gui.LightIndicatorContainer.parentWidget(), toggle=False)
            self.Step_Light.Set_Processing_False(1, self.gui.LightIndicatorContainer.parentWidget(), toggle=True)
            
            self.gui.SubScreens_Measure.setCurrentWidget(self.gui.SubScreen_Measure_Step1_Error)

    def check_devices(self):
        fc500_override = True
        esp_override = True

        if esp_override == True:
            self.logger.log_info("Measure: SYMULACJA - połączenie nawiązane sztucznie z mikrokontrolerem ESP")
        if fc500_override:
            self.logger.log_info("Measure: SYMULACJA - połączenie nawiązane sztucznie z siłomierzem FC500")

        try:
            if fc500_override == True or self.FC500.connection_check():
                self.logger.log_info("Measure: Połączenie nawiązane z FC500")
                self.Step_Light.Set_True("1_1", self.gui.dsp_MeasureProgress_Step_1_1.parentWidget())
                self.fc500_connected = True
            else:
                self.logger.log_error("Measure: Brak połączenia z FC500")
        except Exception as e:
            self.logger.log_error(f"Measure: Błąd podczas sprawdzania połączenia z FC500: {e}")
        try:
            status, message = self.ESP.connect()
            if esp_override == True or status:
                self.logger.log_info("Measure: Połączenie nawiązane z mikrokontrolerem ESP")
                self.Step_Light.Set_True("1_2", self.gui.dsp_MeasureProgress_Step_1_2.parentWidget())
                self.esp_connected = True
            else:
                self.logger.log_error(f"Measure: Brak połączenia z ESP - {message}")
        except Exception as e:
            self.logger.log_error(f"Measure: Błąd podczas sprawdzania połączenia z ESP: {e}")        
    
    def Step2(self):
        self.logger.log_info("Measure Process: Step2")
        QTimer.singleShot(2000, lambda:(self.gui.btn_Measure_Step2_LockSafety.setEnabled(True)))


    def StopCycle(self):
        self.logger.log_warning("Measure process aborted!")
        self.gui.SubScreens_Measure.setCurrentWidget(self.gui.SubScreen_Measure_Step1)
        self.gui.btn_Measure_Step2_LockSafety.setEnabled(True)
        self.Step_Light.Set_Empty("1_1", self.gui.dsp_MeasureProgress_Step_1_1.parentWidget())
        self.Step_Light.Set_Empty("2_1", self.gui.dsp_MeasureProgress_Step_2_1.parentWidget())
        self.Step_Light.Set_Processing("2_1", self.gui.dsp_MeasureProgress_Step_2_1.parentWidget(), toggle=False)
        self.Step_Light.Set_Empty("2_1", self.gui.dsp_MeasureProgress_Step_1_1.parentWidget())
        self.Step_Light.Set_Processing(1, self.gui.LightIndicatorContainer.parentWidget(), toggle=False)
        self.Step_Light.Set_Empty(1, self.gui.LightIndicatorContainer.parentWidget())

    def Refresh(self):
        self.ESP.close()
        self.Step_Light.Set_Empty("1_1", self.gui.dsp_MeasureProgress_Step_1_2.parentWidget())
        self.Step_Light.Set_Empty("1_2", self.gui.dsp_MeasureProgress_Step_1_2.parentWidget())
        #self.measureProcess.check_devices()
        #QTimer.singleShot(1700, lambda:(self.measureProcess.Step1()))
        QTimer.singleShot(1700, lambda:(self.Step1()))