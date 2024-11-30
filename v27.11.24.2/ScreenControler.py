from PySide6.QtWidgets import QWidget

class ScreenController:
    def __init__(self, main_window, ui):
        self.main_window = main_window
        self.ui = ui

        #Button Connections
        self.ui.btn_Measure.clicked.connect(self.show_ScreenMeasureMain)
        self.ui.btn_Graphs.clicked.connect(self.show_ScreenGraphs)
        self.ui.btn_Settings.clicked.connect(self.show_ScreenSettings)
        self.ui.btn_Errors.clicked.connect(self.show_ScreenErrors)

        #Initialize
        self.Screen_MeasureMain = QWidget()
        self.Screen_MeasureProgress = QWidget()
        self.Screen_Graphs = QWidget()
        self.Screen_Settings = QWidget()
        self.Screen_Errors = QWidget()

        #Default Screen - will be logo
        self.current_screen = None
        self.show_ScreenMeasureMain()

    def show_ScreenMeasureMain(self):
        if self.current_screen:
            self.current_screen.hide()
        self.Screen_MeasureMain.show()
        self.current_screen = self.Screen_MeasureMain

    def show_ScreenMeasureMain(self):
        if self.current_screen:
            self.current_screen.hide()
        self.Screen_MeasureMain.show()
        self.current_screen = self.Screen_MeasureMain

    def show_ScreenGraphs(self):
        if self.current_screen:
            self.current_screen.hide()
        self.Screen_Graphs.show()
        self.current_screen = self.Screen_Graphs

    def show_ScreenSettings(self):
        if self.current_screen:
            self.current_screen.hide()
        self.Screen_Settings.show()
        self.current_screen = self.Screen_Settings

    def show_ScreenErrors(self):
        if self.current_screen:
            self.current_screen.hide()
        self.Screen_Errors.show()
        self.current_screen = self.Screen_Errors