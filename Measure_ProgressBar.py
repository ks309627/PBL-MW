from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, QTimer
from LoggingHandler import Logger

class Step_Measure:
    def __init__(self):
        self.logger = Logger()
        self.timers = {}

    def Set_Empty(self, disp_number, parent):
        button_name = f"dsp_MeasureProgress_Step_{disp_number}"
        button = parent.findChild(QPushButton, button_name)
        if button:
            icon = QIcon()
            icon.addFile(u":/Progress/progress/Empty.png", QSize(), QIcon.Mode.Disabled, QIcon.State.Off)
            button.setIcon(icon)
        else:
            self.logger.log_warning("Nie znaleziono przycisku")

    def Set_True(self, disp_number, parent):
        button_name = f"dsp_MeasureProgress_Step_{disp_number}"
        button = parent.findChild(QPushButton, button_name)
        if button:
            icon = QIcon()
            icon.addFile(u":/Progress/progress/True.png", QSize(), QIcon.Mode.Disabled, QIcon.State.Off)
            button.setIcon(icon)
        else:
            self.logger.log_warning("Nie znaleziono przycisku")
            
    def Set_False(self, disp_number, parent):
        button_name = f"dsp_MeasureProgress_Step_{disp_number}"
        button = parent.findChild(QPushButton, button_name)
        if button:
            icon = QIcon()
            icon.addFile(u":/Progress/progress/False.png", QSize(), QIcon.Mode.Disabled, QIcon.State.Off)
            button.setIcon(icon)
        else:
            self.logger.log_warning("Nie znaleziono przycisku")
    
    def Set_Processing_True(self, disp_number, parent, toggle=True):
        button_name = f"dsp_MeasureProgress_Step_{disp_number}"
        button = parent.findChild(QPushButton, button_name)
        if button:
            icon1 = QIcon()
            icon1.addFile(u":/Progress/progress/True.png", QSize(), QIcon.Mode.Disabled, QIcon.State.Off)
            icon2 = QIcon()
            icon2.addFile(u":/Progress/progress/Processing.png", QSize(), QIcon.Mode.Disabled, QIcon.State.Off)

            if toggle:
                if disp_number not in self.timers:
                    self.timers[disp_number] = QTimer()
                    self.timers[disp_number].timeout.connect(lambda disp_number=disp_number, parent=parent: self._toggle_icon(disp_number, parent, icon1, icon2))
                self.timers[disp_number].start(500)
            else:
                if disp_number in self.timers:
                    self.timers[disp_number].stop()
                    del self.timers[disp_number]
                button.setIcon(icon1)
        else:
            self.logger.log_warning("Nie znaleziono przycisku")

    def Set_Processing_False(self, disp_number, parent, toggle=True):
        button_name = f"dsp_MeasureProgress_Step_{disp_number}"
        button = parent.findChild(QPushButton, button_name)
        if button:
            icon1 = QIcon()
            icon1.addFile(u":/Progress/progress/False.png", QSize(), QIcon.Mode.Disabled, QIcon.State.Off)
            icon2 = QIcon()
            icon2.addFile(u":/Progress/progress/Processing.png", QSize(), QIcon.Mode.Disabled, QIcon.State.Off)

            if toggle:
                if disp_number not in self.timers:
                    self.timers[disp_number] = QTimer()
                    self.timers[disp_number].timeout.connect(lambda disp_number=disp_number, parent=parent: self._toggle_icon(disp_number, parent, icon2, icon1))
                self.timers[disp_number].start(500)
            else:
                if disp_number in self.timers:
                    self.timers[disp_number].stop()
                    del self.timers[disp_number]
                button.setIcon(icon1)
        else:
            self.logger.log_warning("Nie znaleziono przycisku")

    def Set_Processing(self, disp_number, parent, toggle=True):
        button_name = f"dsp_MeasureProgress_Step_{disp_number}"
        button = parent.findChild(QPushButton, button_name)
        if button:
            icon1 = QIcon()
            icon1.addFile(u":/Progress/progress/Empty.png", QSize(), QIcon.Mode.Disabled, QIcon.State.Off)
            icon2 = QIcon()
            icon2.addFile(u":/Progress/progress/Processing.png", QSize(), QIcon.Mode.Disabled, QIcon.State.Off)

            if toggle:
                if disp_number not in self.timers:
                    self.timers[disp_number] = QTimer()
                    self.timers[disp_number].timeout.connect(lambda disp_number=disp_number, parent=parent: self._toggle_icon(disp_number, parent, icon1, icon2))
                self.timers[disp_number].start(500)
            else:
                if disp_number in self.timers:
                    self.timers[disp_number].stop()
                    del self.timers[disp_number]
                button.setIcon(icon1)
        else:
            self.logger.log_warning("Nie znaleziono przycisku")

    def _toggle_icon(self, disp_number, parent, icon1, icon2):
        button_name = f"dsp_MeasureProgress_Step_{disp_number}"
        button = parent.findChild(QPushButton, button_name)
        if button:
            current_icon = button.icon()
            if current_icon.cacheKey() == icon2.cacheKey():
                button.setIcon(icon1)
            else:
                button.setIcon(icon2)

    