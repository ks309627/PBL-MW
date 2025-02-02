import os
import re
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QListView
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon

from settings import Settings
from gui_ui import Ui_Main
from LoggingHandler import Logger

class GraphList:
    def __init__(self, gui:Ui_Main, settings: Settings):
        self.settings = settings
        self.logger = Logger()
        self.path = self.settings.get("graphSavePath")
        self.model = QStandardItemModel()
        self.default_icon = QIcon()
        self.default_icon.addFile(u":/Menu/menu/Graph.png", QSize())
        self.view = QListView()
        self.listView = gui.list_graph
        self.listView.setModel(self.model)
        self.load_graphs()

    def load_graphs(self):
        self.model.setRowCount(0)
        folders = [folder for folder in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, folder))]
        for folder in reversed(folders):
            folder_path = os.path.join(self.path, folder)
            if os.path.isdir(folder_path):
                match = re.match(r'measurement_(\d{4}-\d{2}-\d{2})_(\d{2}-\d{2}-\d{2})', folder)
                if match:
                    date_str = match.group(1)
                    time_str = match.group(2)
                    date_time_str = f"{date_str.replace('-', '.')} {time_str.replace('-', ':')}"
                    display_name = f"Pomiar [{date_time_str}]"
                else:
                    display_name = folder

                icon_path = self.find_icon(folder_path)
                item = QStandardItem(display_name)
                if icon_path:
                    item.setIcon(QIcon(icon_path))
                else:
                    item.setIcon(self.default_icon)
                self.model.appendRow(item)
        self.listView.setModel(self.model)

    def find_icon(self, folder_path):
        image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']
        files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
        for file in files:
            if os.path.splitext(file)[1].lower() in image_extensions:
                return os.path.join(folder_path, file).replace('\\', '/')
        return None


