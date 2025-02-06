from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Qt
from PySide6 import QtCharts
from gui_ui import Ui_Main
import json
import os
from datetime import datetime
from settings import Settings
from LoggingHandler import Logger

class GraphControler(QMainWindow):
    def __init__(self, gui:Ui_Main, settings: Settings):
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

    def default_load(self):
        try:
            files = [os.path.join(self.folder_path, f) for f in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, f))]
            if not files:
                self.logger.log_warning(f"No files found in folder {self.folder_path}.")
                return
            most_recent_file = max(files, key=os.path.getctime)
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
        for axis in self.Graph.axes():
            self.Graph.removeAxis(axis)

        self.series = QtCharts.QLineSeries()
        for i, s in enumerate(self.force):
            self.series.append(self.seconds[i], s)
        self.Graph.addSeries(self.series)

        if self.seconds:
            axis_x = QtCharts.QValueAxis()
            axis_x.setRange(min(self.seconds), max(self.seconds))
            axis_x.setTickCount(10)  # Set the number of ticks on the x-axis
            self.Graph.addAxis(axis_x, Qt.AlignBottom)
            self.series.attachAxis(axis_x)

            axis_y = QtCharts.QValueAxis()
            axis_y.setRange(min(self.force) - 1, max(self.force) + 1)
            self.Graph.addAxis(axis_y, Qt.AlignLeft)
            self.series.attachAxis(axis_y)

            # Set the visible range of the x-axis to the last 3 seconds
            if max(self.seconds) - min(self.seconds) > 5:
                axis_x.setRange(max(self.seconds) - 5, max(self.seconds))

        #gui.dsp_graph.setChart(self.Graph)
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




# OLDDDDDD

    def save_graph(self):

        graph_data = {"sekundy": self.seconds, "siła": self.force}
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        save_path = self.settings.get_graph_save_path()
        file_path = os.path.join(save_path, f"{timestamp}.json")

        try:
            with open(file_path, "w") as file:
                json.dump(graph_data, file, indent=4)
            self.logger.log_info(f"Wykres zapisany do: {file_path}")

        except Exception as e:
            self.logger.log_error(f"Wystąpił błąd podczas zapisu wykresu: {e}")

    def load_graph(self, file_path):
        try:
            with open(file_path, "r") as file:
                graph_data = json.load(file)
            self.update_graph_from_data(graph_data["sekundy"], graph_data["siła"])
            self.logger.log_info(f"Wykres załadowany z: {file_path}")
        except Exception as e:
            self.logger.log_error(f"Wystąpił błąd podczas załadowania wykresu: {e}")