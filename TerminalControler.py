import os
import glob
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Qt, QTimer, QEvent, Qt
from PySide6.QtGui import QTextCursor
from gui_ui import Ui_Main
from datetime import datetime
from LoggingHandler import Logger
from CommandHandler import CommandInterpreter
from settings import Settings
from LoginDialog import LoginDialog

class TerminalControler(QMainWindow):
    def __init__(self, gui:Ui_Main, settings:Settings):
        super().__init__()
        self.gui = gui
        self.logger = Logger()
        self.Text = ""
        self.text_edit_basic = gui.terminal_basic
        self.text_edit_admin = gui.terminal_admin
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.Refresh_Loop)

        self.gui.terminal_typefield_admin.returnPressed.connect(self.Send_Command_admin)
        self.CommandReceiver = CommandInterpreter(settings)
        self.settings = settings

        self.command_history = []
        self.command_history_index = 0
        self.gui.terminal_typefield_admin.installEventFilter(self)

    def read_log_file(self, text_edit, file_path=None):
        try:
            if file_path is None:
                log_files = glob.glob('logs/log_*.log')
                if not log_files:
                    self.logger.log_warning("No log files found in the 'logs' directory.")
                    return
                file_path = max(log_files, key=os.path.getctime)
            elif file_path == 'logs/JoinedLogs.log':
                self.logger.join_logs(file_path)

            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                lines = file.readlines()
                reversed_lines = lines[::-1]

                # Define a dictionary to map message types to styles
                style_map = {
                    'USER': {'color': '#444444', 'bold': False},
                    'DEBUG': {'color': '#00B6D5', 'bold': False},
                    'INFO': {'color': '#3E78FF', 'bold': False},
                    'WARNING': {'color': '#E2CD2B', 'bold': True},
                    'ERROR': {'color': '#FF7F00', 'bold': True},
                    'CRITICAL': {'color': '#FF0000', 'bold': True}
                }

                # Initialize an empty string to store the HTML formatted text
                html_text = ''

                # Iterate over each line and format it according to the message type
                for line in reversed_lines:
                    components = line.split(' - ')
                    if len(components) >= 4:
                        message_type = components[2]
                        for style_type, style in style_map.items():
                            if message_type == style_type:
                                font_weight = 'bold' if style['bold'] else 'normal'
                                html_text += f'<font color="{style["color"]}" style="font-weight: {font_weight}">{line.rstrip()}</font><br>'
                                break
                        else:
                            # If no message type is found, use black color by default
                            html_text += f'<font color="#000000">{line.rstrip()}</font><br>'
                    else:
                        # If the line doesn't have the expected format, use black color by default
                        html_text += f'<font color="#000000">{line.rstrip()}</font><br>'

                scrollbar_position = text_edit.verticalScrollBar().value()
                text_edit.setHtml(html_text)
                max_scrollbar_position = text_edit.verticalScrollBar().maximum()
                text_edit.verticalScrollBar().setValue(min(scrollbar_position, max_scrollbar_position))
        except Exception as e:
            self.logger.log_error(f"An error occurred while reading the file: {str(e)}")

    def Refresh_Loop(self):
        try:
            if self.gui.SubScreens_Errors.currentWidget() == self.gui.SubScreen_Errors_Basic:
                if self.gui.btn_Errors_Refresh_basic.isChecked():
                    self.refresh_timer.start(10)
                    self.Perform_Refresh()
                else:
                    self.refresh_timer.stop()
            elif self.gui.SubScreens_Errors.currentWidget() == self.gui.SubScreen_Errors_Admin:
                if self.gui.btn_Errors_Refresh_admin.isChecked():
                    self.refresh_timer.start(10)
                    self.Perform_Refresh()
                else:
                    self.refresh_timer.stop()
            else:
                return
        except Exception as e:
            self.logger.log_error(f"An error occurred while initializing refresh loop: {str(e)}")

    def Perform_Refresh(self):
        if self.settings.get("devMode") == 1:
            self.gui.SubScreens_Errors.setCurrentWidget(self.gui.SubScreen_Errors_Admin)
        else:
            self.gui.SubScreens_Errors.setCurrentWidget(self.gui.SubScreen_Errors_Basic)
        try:
            if self.gui.SubScreens_Errors.currentWidget() == self.gui.SubScreen_Errors_Basic:
                try:
                    if self.gui.btn_Errors_InstanceHistory_basic.isChecked():
                        self.read_log_file(self.text_edit_basic)
                    elif self.gui.btn_Errors_AllHistory_basic.isChecked():
                        self.read_log_file(self.text_edit_basic, 'logs/JoinedLogs.log')
                except Exception as e:
                    self.logger.log_error(f"An error occured while trying to refresh basic terminal: {str(e)}")
            elif self.gui.SubScreens_Errors.currentWidget() == self.gui.SubScreen_Errors_Admin:
                try:
                    if self.gui.btn_Errors_InstanceHistory_admin.isChecked():
                        self.read_log_file(self.text_edit_admin)
                    elif self.gui.btn_Errors_AllHistory_admin.isChecked():
                        self.read_log_file(self.text_edit_admin, 'logs/JoinedLogs.log')
                except Exception as e:
                    self.logger.log_error(f"An error occured while trying to refresh administrator terminal: {str(e)}")
        except Exception as e:
            self.logger.log_error(f"An error occured while trying to refresh: {str(e)}")
        return
    
    def eventFilter(self, obj, event):
        if obj == self.gui.terminal_typefield_admin and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Up:
                if self.command_history:
                    self.command_history_index = max(0, self.command_history_index - 1)
                    self.gui.terminal_typefield_admin.setText(self.command_history[self.command_history_index])
                    return True
            elif event.key() == Qt.Key_Down:
                if self.command_history:
                    self.command_history_index = min(len(self.command_history), self.command_history_index + 1)
                    if self.command_history_index == len(self.command_history):
                        self.gui.terminal_typefield_admin.setText("")
                    else:
                        self.gui.terminal_typefield_admin.setText(self.command_history[self.command_history_index])
                    return True
        return False

    def Send_Command_admin(self):
        command = self.gui.terminal_typefield_admin.text()
        if command:
            self.logger.log_user(command)
            if command.startswith('/'):
                self.CommandReceiver.receiver(command[1:])
            self.Perform_Refresh()
            self.command_history.append(command)
            self.command_history_index = len(self.command_history)
            self.gui.terminal_typefield_admin.setText("")