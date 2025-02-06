from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt
from PySide6 import QtCharts
from gui_ui import Ui_Main

import json
import os
import shutil
from datetime import datetime
from settings import Settings

from LoggingHandler import Logger

class GraphControler(QMainWindow):
    _instance = None

    def __new__(cls, gui: Ui_Main, settings: Settings):
        if cls._instance is None:
            cls._instance = super(GraphControler, cls).__new__(cls)
            cls._instance.__init__(gui, settings)
        return cls._instance

    def __init__(self, gui: Ui_Main, settings: Settings):
        if not hasattr(self, 'initialized'):
            super().__init__()
            self.logger = Logger()
            self.Graph = QtCharts.QChart()
            self.Graph.setTitle("Wykres siły w czasie")
            self.current_offset = 0
            self.gui = gui
            self.settings = settings
            self.folder_path = self.settings.get("graphSavePath")
            if not os.path.exists(self.folder_path):
                os.makedirs(self.folder_path)
            self.seconds = [0, 1]
            self.force = [0, 0]
            self.selected_graph = 0
            self.initialized = True

    def load_graph(self, selected_graph):
        self.selected_graph = selected_graph

        try:
            subdirectories = [os.path.join(self.folder_path, d) for d in os.listdir(self.folder_path) if os.path.isdir(os.path.join(self.folder_path, d))]
            if not subdirectories:
                self.logger.log_warning(f"No subdirectories found in folder {self.folder_path}.")
                return
            subdirectories.sort(key=os.path.getctime, reverse=True)
            if self.selected_graph < 0 or self.selected_graph >= len(subdirectories):
                self.logger.log_error(f"Invalid graph index {self.selected_graph}.")
                return

            selected_subdirectory = subdirectories[self.selected_graph]

            files = [os.path.join(selected_subdirectory, f) for f in os.listdir(selected_subdirectory) if os.path.isfile(os.path.join(selected_subdirectory, f))]

            json_files = [file for file in files if file.endswith('.json')]
            if json_files:
                most_recent_file = max(json_files, key=os.path.getctime)
            else:
                self.logger.log_warning(f"No graph file found in subdirectory {selected_subdirectory}.")
                return

            with open(most_recent_file, 'r') as file:
                data = json.load(file)
                self.seconds = data['seconds']
                self.force = [float(value.replace(" ", "").replace("N", "")) for value in data['force']]
                self.default_update_graph(self.gui)
        except json.JSONDecodeError:
            self.logger.log_error(f"Failed to parse JSON in file {most_recent_file}.")
        except KeyError:
            self.logger.log_error(f"Invalid JSON format in file {most_recent_file}.")

    def default_update_graph(self, gui: Ui_Main):
        self.Graph.removeAllSeries()
        for self.axis in self.Graph.axes():
            self.Graph.removeAxis(self.axis)

        self.series = QtCharts.QLineSeries()
        for i, s in enumerate(self.force):
            self.series.append(self.seconds[i], s)
        self.Graph.addSeries(self.series)

        if self.seconds:
            self.axis_x = QtCharts.QValueAxis()
            self.axis_x.setRange(min(self.seconds), max(self.seconds))
            self.axis_x.setTickCount(10)
            self.Graph.addAxis(self.axis_x, Qt.AlignBottom)
            self.series.attachAxis(self.axis_x)

            axis_y = QtCharts.QValueAxis()
            axis_y.setRange(min(self.force) - 1, max(self.force) + 1)
            self.Graph.addAxis(axis_y, Qt.AlignLeft)
            self.series.attachAxis(axis_y)

            # Set the visible range of the x-axis to the last 5 seconds
            if max(self.seconds) - min(self.seconds) > 5:
                self.axis_x.setRange(max(self.seconds) - 5, max(self.seconds))

        gui.dsp_graph.setChart(self.Graph)
        gui.dsp_graph_2.setChart(self.Graph)


    def scroll_left(self):
        axis_x = self.Graph.axes(Qt.Horizontal)[0]
        min_val = axis_x.min()
        max_val = axis_x.max()
        range_val = max_val - min_val
        axis_x.setRange(min_val - range_val / 10, max_val - range_val / 10)

    def scroll_right(self):
        axis_x = self.Graph.axes(Qt.Horizontal)[0]
        min_val = axis_x.min()
        max_val = axis_x.max()
        range_val = max_val - min_val
        axis_x.setRange(min_val + range_val / 10, max_val + range_val / 10)

    def scroll_up(self):
        axis_y = self.Graph.axes(Qt.Vertical)[0]
        min_val = axis_y.min()
        max_val = axis_y.max()
        range_val = max_val - min_val
        axis_y.setRange(min_val + range_val / 10, max_val + range_val / 10)

    def scroll_down(self):
        axis_y = self.Graph.axes(Qt.Vertical)[0]
        min_val = axis_y.min()
        max_val = axis_y.max()
        range_val = max_val - min_val
        axis_y.setRange(min_val - range_val / 10, max_val - range_val / 10)

    def zoom_in(self):
        axis_x = self.Graph.axes(Qt.Horizontal)[0]
        axis_y = self.Graph.axes(Qt.Vertical)[0]
        x_min_val = axis_x.min()
        x_max_val = axis_x.max()
        x_range_val = x_max_val - x_min_val
        y_min_val = axis_y.min()
        y_max_val = axis_y.max()
        y_range_val = y_max_val - y_min_val
        axis_x.setRange(x_min_val + x_range_val / 20, x_max_val - x_range_val / 20)
        axis_y.setRange(y_min_val + y_range_val / 20, y_max_val - y_range_val / 20)

    def zoom_out(self):
        axis_x = self.Graph.axes(Qt.Horizontal)[0]
        axis_y = self.Graph.axes(Qt.Vertical)[0]
        x_min_val = axis_x.min()
        x_max_val = axis_x.max()
        x_range_val = x_max_val - x_min_val
        y_min_val = axis_y.min()
        y_max_val = axis_y.max()
        y_range_val = y_max_val - y_min_val
        axis_x.setRange(x_min_val - x_range_val / 20, x_max_val + x_range_val / 20)
        axis_y.setRange(y_min_val - y_range_val / 20, y_max_val + y_range_val / 20)

    def reset(self):
        axis_x = self.Graph.axes(Qt.Horizontal)[0]
        axis_y = self.Graph.axes(Qt.Vertical)[0]
        series = self.Graph.series()[0]
        data_points = series.pointsVector()
        min_x = min(point.x() for point in data_points)
        max_x = max(point.x() for point in data_points)
        min_y = min(point.y() for point in data_points)
        max_y = max(point.y() for point in data_points)
        range_x = max_x - min_x
        range_y = max_y - min_y
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        axis_x.setRange(center_x - range_x / 2 * 0.6, center_x + range_x / 2 * 0.6)
        axis_y.setRange(center_y - range_y / 2 * 1.2, center_y + range_y / 2 * 1.2)