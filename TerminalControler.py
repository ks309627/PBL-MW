import os
import glob
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QTextCursor
from gui_ui import Ui_Main
from datetime import datetime
from LoggingHandler import ErrorLogger
from CommandHandler import CommandInterpreter

class TerminalControler(QMainWindow):
    def __init__(self, gui:Ui_Main):
        super().__init__()
        self.gui = gui
        self.error_logger = ErrorLogger()
        self.Text = ""
        self.text_edit_basic = gui.terminal_basic
        self.text_edit_admin = gui.terminal_admin
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.Refresh_Loop)

        self.gui.terminal_typefield_admin.returnPressed.connect(self.Send_Command_admin)
        self.CommandReceiver = CommandInterpreter()

    def SingleLog_basic(self):
        try:
            log_files = glob.glob('logs/log_*.log')
            if not log_files:
                self.error_logger.log_warning("No log files found in the 'logs' directory.")
                return
            most_recent_file = max(log_files, key=os.path.getctime)

            with open(most_recent_file, 'r') as file:
                text = file.read()
                scrollbar_position = self.text_edit_basic.verticalScrollBar().value()
                self.text_edit_basic.setText(text)
                max_scrollbar_position = self.text_edit_basic.verticalScrollBar().maximum()
                self.text_edit_basic.verticalScrollBar().setValue(min(scrollbar_position, max_scrollbar_position))
        except Exception as e:
            self.error_logger.log_error(f"An error occurred while reading the file: {str(e)}")
        
    def JoinedLogs_basic(self):
        try:
            self.error_logger.join_logs('logs/JoinedLogs.log')
            file_path = 'logs/JoinedLogs.log'
            with open(file_path, 'r') as file:
                text = file.read()
                scrollbar_position = self.text_edit_basic.verticalScrollBar().value()
                self.text_edit_basic.setText(text)
                self.text_edit_basic.verticalScrollBar().setValue(scrollbar_position)
        except Exception as e:
            self.error_logger.log_error(f"An error occurred while reading the file: {str(e)}")

    def SingleLog_admin(self):
        try:
            log_files = glob.glob('logs/log_*.log')
            if not log_files:
                self.error_logger.log_warning("No log files found in the 'logs' directory.")
                return
            most_recent_file = max(log_files, key=os.path.getctime)

            with open(most_recent_file, 'r') as file:
                text = file.read()
                scrollbar_position = self.text_edit_admin.verticalScrollBar().value()
                self.text_edit_admin.setText(text)
                max_scrollbar_position = self.text_edit_admin.verticalScrollBar().maximum()
                self.text_edit_admin.verticalScrollBar().setValue(min(scrollbar_position, max_scrollbar_position))
        except Exception as e:
            self.error_logger.log_error(f"An error occurred while reading the file: {str(e)}")
    
    def JoinedLogs_admin(self):
        try:
            self.error_logger.join_logs('logs/JoinedLogs.log')
            file_path = 'logs/JoinedLogs.log'
            with open(file_path, 'r') as file:
                text = file.read()
                scrollbar_position = self.text_edit_admin.verticalScrollBar().value()
                self.text_edit_admin.setText(text)
                self.text_edit_admin.verticalScrollBar().setValue(scrollbar_position)
        except Exception as e:
            self.error_logger.log_error(f"An error occurred while reading the file: {str(e)}")

    def Refresh_Loop(self):
        try:
            if self.gui.Subscreens_Errors.currentWidget() == self.gui.SubScreen_Errors_Basic:
                if self.gui.btn_Errors_Refresh_basic.isChecked():
                    self.refresh_timer.start(10)
                    self.Perform_Refresh()
                else:
                    self.refresh_timer.stop()
            elif self.gui.Subscreens_Errors.currentWidget() == self.gui.SubScreen_Errors_Admin:
                if self.gui.btn_Errors_Refresh_admin.isChecked():
                    self.refresh_timer.start(10)
                    self.Perform_Refresh()
                else:
                    self.refresh_timer.stop()
            else:
                return
        except Exception as e:
            self.error_logger.log_error(f"An error occurred while initializing refresh loop: {str(e)}")

    def Perform_Refresh(self):
        try:
            if self.gui.Subscreens_Errors.currentWidget() == self.gui.SubScreen_Errors_Basic:
                try:
                    if self.gui.btn_Errors_InstanceHistory_basic.isChecked():
                        self.SingleLog_basic()
                    elif self.gui.btn_Errors_AllHistory_basic.isChecked():
                        self.JoinedLogs_basic()
                except Exception as e:
                    self.error_logger.log_error(f"An error occured while trying to refresh basic terminal: {str(e)}")
            elif self.gui.Subscreens_Errors.currentWidget() == self.gui.SubScreen_Errors_Admin:
                try:
                    if self.gui.btn_Errors_InstanceHistory_admin.isChecked():
                        self.SingleLog_admin()
                    elif self.gui.btn_Errors_AllHistory_admin.isChecked():
                        self.JoinedLogs_admin()
                except Exception as e:
                    self.error_logger.log_error(f"An error occured while trying to refresh administrator terminal: {str(e)}")
        except Exception as e:
            self.error_logger.log_error(f"An error occured while trying to refresh: {str(e)}")
        return

    def Send_Command_admin(self):
        command = self.gui.terminal_typefield_admin.text()
        if command:
            self.error_logger.log_user(command)
            self.CommandReceiver.receiver(command)
            self.Perform_Refresh()
            self.gui.terminal_typefield_admin.setText("")