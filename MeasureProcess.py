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


    def safety_unlock(self):
        pass

    def safety_lock(self):
        pass