from PySide6.QtCore import QTimer

from FC500Com import FC500Com
from LoggingHandler import Logger
from gui_ui import Ui_Main
from Measure_ProgressBar import Step_Measure
from settings import Settings
#TMQ from EspCom import connection_checkv czy coś takiego

import asyncio

class MeasureProcess:
    
    def __init__(self, gui:Ui_Main, settings:Settings):
        self.logger = Logger()
        self.gui = gui
        self.Step_Light = Step_Measure()
        self.settings = settings
        self.Step_Flags = 0
        try:
            self.FC500 = FC500Com(settings)
        except:
            self.logger.log_error("Start Up: Nie można połączyć się z FC500. Proszę sprawdzić kabel oraz stan urządzenia. Odłączenie i ponowne podłączenie kabla może być wymagane.")
        #TMQ try except jak wyżej tylko dla esp
        
        self.loop = asyncio.get_event_loop()
        self.cycle = self.loop.create_task(self.MeasureCycle())

    def StopCycle(self):
        self.cycle.cancel()
        self.CycleCleanUp()
        self.logger.log_warning("Measure process aborted!")

    def CycleCleanUp(self):
        self.gui.SubScreens_Measure.setCurrentWidget(self.gui.SubScreen_Measure_Step1)
        self.Step_Light.Set_Empty("1_1", self.gui.dsp_MeasureProgress_Step_1_1.parentWidget())
        self.Step_Light.Set_Empty("1_2", self.gui.dsp_MeasureProgress_Step_1_1.parentWidget())

        parent_widget = self.gui.LightIndicatorContainer.parentWidget()
        toggle = False

        for i in range(1, 5):
            self.Step_Light.Set_Processing(i, parent_widget, toggle)
            self.Step_Light.Set_Processing_True(i, parent_widget, toggle)
            self.Step_Light.Set_Processing_False(i, parent_widget, toggle)
            self.Step_Light.Set_Empty(i, parent_widget)

    async def MeasureCycle(self):
        try:
            while True:
                if self.gui.SubScreens_Measure.currentWidget() == self.gui.SubScreen_Measure_Step1 and self.Step_Flags == 0:
                    self.Step_Flags = 1
                    await self.Measure_Step1()
                elif self.gui.SubScreens_Measure.currentWidget() == self.gui.SubScreen_Measure_Step2 and self.Step_Flags == 1:
                    self.Step_Flags = 2
                    await self.Measure_Step2()
                break
        except Exception as e:
            self.logger.log_error(f"An error occured inside of MeasureCycle: {e}")

    async def Measure_Step1(self):
        self.logger.log_info("Measure Process: Step 1")
        self.gui.btn_Measure_Step1_ObjectReady.setEnabled(False)
        self.Step_Light.Set_Processing(1, self.gui.LightIndicatorContainer.parentWidget(), toggle=True)
        self.gui.SubScreens_Measure.setCurrentWidget(self.gui.SubScreen_Measure_Step1)
        try:
            self.FC500.connection_check()
            if self.FC500.connection_check() == True:
                self.logger.log_info("Measure: Połączenie nawiązane z FC500")
                # try:
                #     pass #TMQ jakiś connection check dla esp + dodać tab poniżej
                if self.gui.SubScreens_Measure.currentWidget() != self.gui.SubScreen_Measure_Step1_Error:
                    await self.safety_unlock()
                    self.Step_Light.Set_Processing(1, self.gui.dsp_MeasureProgress_Step_1.parentWidget(), toggle=False)
                    self.Step_Light.Set_Processing_True(1, self.gui.dsp_MeasureProgress_Step_1.parentWidget(), toggle=True)
                    self.gui.btn_Measure_Step1_ObjectReady.setEnabled(True)
                    self.MeasureCycle()
                # except:
                #     QTimer.singleShot(2000, self.Measure_Step1_ErrorESP)
        except:
            QTimer.singleShot(2000, self.Measure_Step1_ErrorFC)



    def Measure_Step1_ErrorFC(self):
        self.logger.log_error("Measure: Nie można połączyć się z FC500. Proszę sprawdzić kabel oraz stan urządzenia. Odłączenie i ponowne podłączenie kabla lub/oraz restart programu mogą być wymagane.")
        self.Step_Light.Set_Processing(1, self.gui.LightIndicatorContainer.parentWidget(), toggle=False)
        self.Step_Light.Set_Processing_False(1, self.gui.LightIndicatorContainer.parentWidget(), toggle=True)
        self.Step_Light.Set_False("1_1", self.gui.dsp_MeasureProgress_Step_1_1.parentWidget())
        if self.gui.SubScreens_Measure.currentWidget() != self.gui.SubScreen_Measure_Step1_Error:
            self.gui.SubScreens_Measure.setCurrentWidget(self.gui.SubScreen_Measure_Step1_Error)
    
    def Measure_Step1_ErrorESP(self):
        self.logger.log_error("ESP") #TMQ Tu jakiś error pasujący do ESP
        self.Step_Light.Set_Processing(1, self.gui.LightIndicatorContainer.parentWidget(), toggle=False)
        self.Step_Light.Set_Processing_False(1, self.gui.LightIndicatorContainer.parentWidget(), toggle=True)
        self.Step_Light.Set_False("1_2", self.gui.dsp_MeasureProgress_Step_1_1.parentWidget())
        if self.gui.SubScreens_Measure.currentWidget() != self.gui.SubScreen_Measure_Step1_Error:
            self.gui.SubScreens_Measure.setCurrentWidget(self.gui.SubScreen_Measure_Step1_Error)
    
    async def Measure_Step1_Error_Refresh(self):
        try:
            self.FC500.connection_check()
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
        
        
      
    