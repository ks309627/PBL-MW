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
        self.seconds = [0, 1]
        self.force = [0, 0]

        self.default_load()

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
                self.update_graph_data(self.gui)
        except json.JSONDecodeError:
            self.logger.log_error(f"Failed to parse JSON in file {most_recent_file}.")
        except KeyError:
            self.logger.log_error(f"Invalid JSON format in file {most_recent_file}.")


    def update_graph_data(self, gui: Ui_Main):
        self.Graph.removeAllSeries()
        for axis in self.Graph.axes():
            self.Graph.removeAxis(axis)

        self.series = QtCharts.QLineSeries()
        for i, s in enumerate(self.force):
            self.series.append(self.seconds[i], s)

        self.Graph.addSeries(self.series)

        axis_x = QtCharts.QValueAxis()
        axis_x.setRange(self.current_offset + self.seconds[0], self.current_offset + self.seconds[-1])
        self.Graph.addAxis(axis_x, Qt.AlignBottom)
        self.series.attachAxis(axis_x)

        axis_y = QtCharts.QValueAxis()
        axis_y.setRange(self.current_offset + min(self.force) - 1, self.current_offset + max(self.force) + 1)
        self.Graph.addAxis(axis_y, Qt.AlignLeft)
        self.series.attachAxis(axis_y)

        #gui.dsp_graph.setChart(self.Graph)
        gui.dsp_graph_2.setChart(self.Graph)


# OLDDDDDD

    def update_Graph(self, gui: Ui_Main):
        seconds = [0, 1]
        force = [0, 0]

        self.Graph.removeAllSeries()
        for axis in self.Graph.axes():
            self.Graph.removeAxis(axis)

        self.series = QtCharts.QLineSeries()
        for i, s in enumerate(force):
            self.series.append(seconds[i], s)

        self.Graph.addSeries(self.series)

        axis_x = QtCharts.QValueAxis()
        axis_x.setRange(self.current_offset + seconds[0], self.current_offset + seconds[-1])
        self.Graph.addAxis(axis_x, Qt.AlignBottom)
        self.series.attachAxis(axis_x)

        axis_y = QtCharts.QValueAxis()
        axis_y.setRange(self.current_offset + min(force) - 1, self.current_offset + max(force) + 1)
        self.Graph.addAxis(axis_y, Qt.AlignLeft)
        self.series.attachAxis(axis_y)

        #gui.dsp_graph.setChart(self.Graph)
        #gui.dsp_graph_2.setChart(self.Graph)

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

    def update_graph_from_data(self, sekundy, siła):
        self.Graph.removeAllSeries()
        for axis in self.Graph.axes():
            self.Graph.removeAxis(axis)
        self.series = QtCharts.QLineSeries()
        for i, s in enumerate(siła):
            self.series.append(sekundy[i], s)
        self.Graph.addSeries(self.series)

        axis_x = QtCharts.QValueAxis()
        axis_x.setRange(sekundy[0], sekundy[-1])
        self.Graph.addAxis(axis_x, Qt.AlignBottom)
        self.series.attachAxis(axis_x)

        axis_y = QtCharts.QValueAxis()
        axis_y.setRange(min(siła) - 1, max(siła) + 1)
        self.Graph.addAxis(axis_y, Qt.AlignLeft)
        self.series.attachAxis(axis_y)

    def scroll_left(self):
        self.Graph.scroll(-10, 0)

    def scroll_right(self):
        self.Graph.scroll(10, 0)

    def scroll_up(self):
        self.Graph.scroll(0, 10)

    def scroll_down(self):
        self.Graph.scroll(0, -10)

    def zoom_in(self):
        self.Graph.zoomIn()

    def zoom_out(self):
        self.Graph.zoomOut()

    def reset(self):
        self.Graph.zoomReset()
        self.Graph.scroll(0, 0)