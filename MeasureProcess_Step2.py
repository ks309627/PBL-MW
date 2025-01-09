from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from FC500Com import FC500Com
from ESPCom import ESPCom #changed SerialCommunicator to ESPCom
from LoggingHandler import Logger
from gui_ui import Ui_Main
from settings import Settings
from Measure_Lights import Measure_Lights
from GraphLimits import ForceChecker
from MeasureProcess_Step1 import FC500Com, ESPCom

class MeasureProcess_Steps2:
    def __init__(self, gui:Ui_Main, settings:Settings):
        self.logger = Logger()
        self.gui = gui
        self.Step_Light = Measure_Lights()
        self.FC500 = FC500Com(settings)
        self.ESP = ESPCom(settings)
        self.force_checker = ForceChecker()

        self.Step2_forcecheck_loop = 0

    def begin(self):
        self.gui.btn_Measure_Step2_LockSafety.setEnabled(False)
        self.logger.log_info("Measure Process: Step 2")
        self.Step_Light.Set_Processing(2, self.gui.dsp_MeasureProgress_Step_1.parentWidget(), toggle=True)
        self.Step_Light.Set_Processing_True(1, self.gui.dsp_MeasureProgress_Step_1.parentWidget(), toggle=False)
        self.Step_Light.Set_True(1, self.gui.LightIndicatorContainer.parentWidget())
        self.Step_Light.Set_True("2_1", self.gui.dsp_MeasureProgress_Step_2_1.parentWidget())
        self.gui.btn_Measure_Step2_LockSafety.setEnabled(True)

    def Measure_Step2_2(self):
        from MeasureProcess_Step1 import fc500_override

        self.gui.btn_Measure_Step2_LockSafety.setEnabled(False)
        self.logger.log_info("Measure: Safety locked.")
        self.Step_Light.Set_Empty("2_1", self.gui.dsp_MeasureProgress_Step_2_1.parentWidget())
        try:
            self.FC500.cmd_zero()
        except:
            self.logger.log_error("Measure: Lost connection to FC500. Aborting")
            if  fc500_override == False:
                self.StopCycle()
        QTimer.singleShot(1000, lambda:(self.Measure_Step2_3()))

    def Measure_Step2_3(self):
        if self.Step2_forcecheck_loop == 0:
            #ESP TMQ: tu kod który zacznie naprężać próbkę do N kroków / sekund. Jakby się dało to podłączyć pozycję do progress bara który jest w gui.
            pass
        QTimer.singleShot(500, lambda:(self.Measure_Step2_4()))

    def Measure_Step2_4(self):
        self.logger.log_info("Step2_4")
        if self.force_checker.force_check(20):
            self.logger.log_warning("Measure: Force exceeded 20 N. Progressing...")
            self.Step_Light.Set_Processing("2_1", self.gui.dsp_MeasureProgress_Step_2_1.parentWidget(), toggle=False)
            self.Step_Light.Set_True("2_1", self.gui.dsp_MeasureProgress_Step_2_1.parentWidget())
            self.gui.SubScreens_Measure.setCurrentWidget(self.gui.SubScreen_Measure_Step3)
            self.MeasureCycle()
        elif self.Step2_forcecheck_loop < 8:
            self.Step2_forcecheck_loop += 1
            self.logger.log_warning("Measure: Force didn't exceed 20 N. Retrying...")
            self.Step_Light.Set_Processing_False("2_1", self.gui.dsp_MeasureProgress_Step_2_1.parentWidget(), toggle=True)
            self.Measure_Step2_3()
        else:
            self.logger.log_warning("Measure: The object was not detected.")
            self.gui.SubScreens_Measure.setCurrentWidget(self.gui.SubScreen_Measure_Step2_Error)
            self.Step_Light.Set_Processing(2, self.gui.LightIndicatorContainer.parentWidget(), toggle=False)
            self.Step_Light.Set_Processing_False(2, self.gui.LightIndicatorContainer.parentWidget(), toggle=False)