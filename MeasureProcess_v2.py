from PySide6.QtCore import QTimer
from gui_ui import Ui_Main
from FC500Com import FC500Com
from ESPCom import ESPCom
from LoggingHandler import Logger
from Measure_Lights import Measure_Lights
from settings import Settings
from GraphLimits import ForceChecker
from CommandHandler import CommandInterpreter
from GraphJsonHandler import GraphRecorder

class MeasureProcess:
    def __init__(self, gui:Ui_Main, settings:Settings):
        self.settings = settings
        self.gui = gui
        self.logger = Logger()
        self.Step_Light = Measure_Lights()
        
        self.ESP = None
        self.FC500 = None
        self.Step_Flags = 0

        self.val = 0
        self.fc500_connected = False
        self.esp_connected = False

        #self.FC500_command = CommandInterpreter(self.gui, self.settings)
        self.FC500_command = GraphRecorder(self.gui, self.settings)
        self.ForceCheck = ForceChecker()

        self.init_devices()

        self.force_timer = QTimer()
        self.force_timer.timeout.connect(self.measure_check_force)

    def init_devices(self):
        try:
            self.FC500 = FC500Com(self.settings)
            self.logger.log_debug(f"Inicjalizacja FC500 udana")
        except Exception as e:
            self.logger.log_debug(f"Inicjalizacja FC500 nieudana")
        try:
            self.ESP = ESPCom(self.settings)
            self.logger.log_debug(f"Inicjalizacja ESP udana")
        except Exception as e:
            self.logger.log_debug(f"Inicjalizacja FC500 nieudana")

    def begin(self):
        self.logger.log_info("Pomiar: Rozpoczęcie pomiaru")
        self.step_flags = 0
        self.gui.btn_Measure_Step1_ObjectReady.setEnabled(False)
        self.Step_Light.Set_Processing(1, self.gui.LightIndicatorContainer.parentWidget(), toggle=True)
        self.gui.SubScreens_Measure.setCurrentWidget(self.gui.SubScreen_Measure_Step1)
        self.fc500_connected = False
        self.esp_connected = False
        QTimer.singleShot(1700, lambda:(self.Step1()))

    def Step1(self):
        #self.init_devices()

        self.gui.SubScreens_Measure.setCurrentWidget(self.gui.SubScreen_Measure_Step1)

        self.logger.log_info("Pomiar: Krok 1 - Sprawdzenie podłączenia fiłomierza FC500 i mikrokontrolera ESP")
        self.check_devices()

        if self.fc500_connected and self.esp_connected:
            self.logger.log_info("Pomiar: Oba urządzenia są podłączone, przejście do Kroku 2")
            self.Step_Light.Set_Processing(1, self.gui.dsp_MeasureProgress_Step_1.parentWidget(), toggle=False)
            self.Step_Light.Set_Processing_True(1, self.gui.dsp_MeasureProgress_Step_1.parentWidget(), toggle=True)
            self.gui.btn_Measure_Step1_ObjectReady.setEnabled(True)
            self.Step2()
        if not self.fc500_connected:
            # if self.esp_connected:
            #     self.Step_Light.Set_True("1_2", self.gui.dsp_MeasureProgress_Step_1_2.parentWidget())
            self.logger.log_error("Pomiar: Nie można połączyć się z FC500. Proszę sprawdzić kabel oraz stan urządzenia. Odłączenie i ponowne podłączenie kabla lub/oraz restart programu mogą być wymagane")
            self.Step_Light.Set_False("1_1", self.gui.dsp_MeasureProgress_Step_1_1.parentWidget())
            self.Step_Light.Set_Processing(1, self.gui.LightIndicatorContainer.parentWidget(), toggle=False)
            self.Step_Light.Set_Processing_False(1, self.gui.LightIndicatorContainer.parentWidget(), toggle=True)
            self.gui.SubScreens_Measure.setCurrentWidget(self.gui.SubScreen_Measure_Step1_Error)          
        if not self.esp_connected:
            # if self.fc500_connected:
            #     self.Step_Light.Set_True("1_1", self.gui.dsp_MeasureProgress_Step_1_2.parentWidget())
            self.logger.log_error("Pomiar: Nie można połączyć się z mikrokontrolerem ESP. Proszę sprawdzić stan podłączenia przewodów. Odłączenie i ponowne podłączenie kabla lub/oraz restart programu mogą być wymagane")
            self.Step_Light.Set_False("1_2", self.gui.dsp_MeasureProgress_Step_1_2.parentWidget())
            self.Step_Light.Set_Processing(1, self.gui.LightIndicatorContainer.parentWidget(), toggle=False)
            self.Step_Light.Set_Processing_False(1, self.gui.LightIndicatorContainer.parentWidget(), toggle=True)
            
            self.gui.SubScreens_Measure.setCurrentWidget(self.gui.SubScreen_Measure_Step1_Error)

    def check_devices(self):
        fc500_override = False
        esp_override = False
        if esp_override:
            self.logger.log_debug("Pomiar: SYMULACJA połączenia z mikrokontrolerem ESP")
        if fc500_override:
            self.logger.log_debug("Pomiar: SYMULACJA połączenia z siłomierzem FC500")

        try:
            if fc500_override == True or self.FC500.connection_check():
                if fc500_override == False:
                    self.logger.log_info("Pomiar: Połączenie nawiązane z FC500")
                self.Step_Light.Set_True("1_1", self.gui.dsp_MeasureProgress_Step_1_1.parentWidget())
                self.fc500_connected = True
            else:
                self.logger.log_error("Pomiar: Brak połączenia z FC500")
        except Exception as e:
            self.logger.log_error(f"Pomiar: Błąd podczas sprawdzania połączenia z FC500: {e}")
        try:
            status, message = self.ESP.connect()
            if esp_override == True or status:
                if esp_override == False:
                    self.logger.log_info("Pomiar: Połączenie nawiązane z mikrokontrolerem ESP")
                self.Step_Light.Set_True("1_2", self.gui.dsp_MeasureProgress_Step_1_2.parentWidget())
                self.esp_connected = True
            else:
                self.logger.log_error(f"Pomiar: Brak połączenia z ESP - {message}")
        except Exception as e:
            self.logger.log_error(f"Pomiar: Błąd podczas sprawdzania połączenia z ESP: {e}")        
    
    def Step2(self):
        self.logger.log_info("Pomiar: Krok 2 - próbne rozciąganie próbki")
        self.Step_Light.Set_Processing(1, self.gui.LightIndicatorContainer.parentWidget(), toggle=False)
        self.Step_Light.Set_True(1, self.gui.LightIndicatorContainer.parentWidget())
        self.Step_Light.Set_Processing(2, self.gui.LightIndicatorContainer.parentWidget(), toggle=True)
        self.ESP.cmd_custom(str(40))

        QTimer.singleShot(3000, lambda:(self.gui.btn_Measure_Step2_LockSafety.setEnabled(True)))

    def Step3(self):
        self.logger.log_info("Pomiar: Krok 3 - rozpoczęcie pomiaru")
        self.Step_Light.Set_Processing(2, self.gui.LightIndicatorContainer.parentWidget(), toggle=False)
        self.Step_Light.Set_True(2, self.gui.LightIndicatorContainer.parentWidget())
        self.Step_Light.Set_Processing(3, self.gui.LightIndicatorContainer.parentWidget(), toggle=True)      

        self.FC500_command.graphMeasure_process(15)
        self.start_force_check()

    def Step4(self):
        self.logger.log_info("Measure Process: Step4")
        self.Step_Light.Set_Processing(4, self.gui.LightIndicatorContainer.parentWidget(), toggle=False)
        self.Step_Light.Set_True(4, self.gui.LightIndicatorContainer.parentWidget())

    def StopCycle(self):
        self.logger.log_warning("Pomiar: Proces został zakończony")
        self.gui.SubScreens_Measure.setCurrentWidget(self.gui.SubScreen_Measure_Step1)
        self.gui.btn_Measure_Step2_LockSafety.setEnabled(True)
        self.Step_Light.Set_Empty("1_1", self.gui.dsp_MeasureProgress_Step_1_1.parentWidget())
        self.Step_Light.Set_Empty("2_1", self.gui.dsp_MeasureProgress_Step_2_1.parentWidget())
        self.Step_Light.Set_Processing("2_1", self.gui.dsp_MeasureProgress_Step_2_1.parentWidget(), toggle=False)
        self.Step_Light.Set_Empty("2_1", self.gui.dsp_MeasureProgress_Step_1_1.parentWidget())
        self.Step_Light.Set_Processing(1, self.gui.LightIndicatorContainer.parentWidget(), toggle=False)
        self.Step_Light.Set_Processing(2, self.gui.LightIndicatorContainer.parentWidget(), toggle=False)
        self.Step_Light.Set_Processing(3, self.gui.LightIndicatorContainer.parentWidget(), toggle=False)
        self.Step_Light.Set_Processing(4, self.gui.LightIndicatorContainer.parentWidget(), toggle=False)
        self.Step_Light.Set_Empty(1, self.gui.LightIndicatorContainer.parentWidget())
        self.Step_Light.Set_Empty(2, self.gui.LightIndicatorContainer.parentWidget())
        self.Step_Light.Set_Empty(3, self.gui.LightIndicatorContainer.parentWidget())
        self.Step_Light.Set_Empty(4, self.gui.LightIndicatorContainer.parentWidget())

    def Refresh(self):
        self.ESP.connection_close()
        self.Step_Light.Set_Empty("1_1", self.gui.dsp_MeasureProgress_Step_1_2.parentWidget())
        self.Step_Light.Set_Empty("1_2", self.gui.dsp_MeasureProgress_Step_1_2.parentWidget())
        QTimer.singleShot(1700, lambda:(self.Step1()))

    def measure_check_force(self):
        if self.ForceCheck.force_check(1):
            print("Warunek spełniony, kontynuuję...")
        else:
            print("Warunek niespełniony, zatrzymanie procesu.")
            self.force_timer.stop()
            self.FC500_command.graphMeasure_process("stop")
            self.gui.btn_Measure_Step3.setEnabled(True)

            self.Step_Light.Set_Processing(3, self.gui.LightIndicatorContainer.parentWidget(), toggle=False)
            self.Step_Light.Set_True(3, self.gui.LightIndicatorContainer.parentWidget())
            self.Step_Light.Set_Processing(4, self.gui.LightIndicatorContainer.parentWidget(), toggle=True)

    def start_force_check(self):
        print("Rozpoczęcie cyklicznego sprawdzania warunku...")
        self.force_timer.start(1000)

    def stop_force_check(self):
        print("Zatrzymanie cyklicznego sprawdzania warunku.")
        self.force_timer.stop()

    def tension_check_force(self):
        if self.ForceCheck.force_check(3):
            print("element został wykryty")
        else:
            print("nie wykryto elementu")

    def send_esp_command_r1(self):
        self.ESP.cmd_custom(str(1))
    def send_esp_command_r2(self):
        self.ESP.cmd_custom(str(5))
    def send_esp_command_r3(self):
        self.ESP.cmd_custom(str(20))
    def send_esp_command_l1(self):
        self.ESP.cmd_custom(str(-1))
    def send_esp_command_l2(self):
        self.ESP.cmd_custom(str(-5))
    def send_esp_command_l3(self):
        self.ESP.cmd_custom(str(-20))