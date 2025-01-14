from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Qt
from PySide6 import QtCharts
from gui_ui import Ui_Main
import json
from datetime import datetime
from settings import Settings
import os
from LoggingHandler import Logger

class GraphControler(QMainWindow):
    def __init__(self, gui:Ui_Main, settings: Settings):
        super().__init__()
        self.logger = Logger()
        self.Graph = QtCharts.QChart()
        self.Graph.setTitle("Wykres siły w czasie")
        self.current_offset = 0
        self.gui = gui
        self.update_Graph(gui)
        self.settings = settings # v03.01.25.1


    def update_Graph(self, gui: Ui_Main):
        sekundy = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        siła = [10, 13, 15, 18, 21, 23, 24, 25, 25, 20, 0, 0, 0]

        self.Graph.removeAllSeries()
        for axis in self.Graph.axes():
            self.Graph.removeAxis(axis)

        self.series = QtCharts.QLineSeries()
        for i, s in enumerate(siła):
            self.series.append(sekundy[i], s)

        self.Graph.addSeries(self.series)

        axis_x = QtCharts.QValueAxis()
        axis_x.setRange(self.current_offset + sekundy[0], self.current_offset + sekundy[-1])
        self.Graph.addAxis(axis_x, Qt.AlignBottom)
        self.series.attachAxis(axis_x)

        axis_y = QtCharts.QValueAxis()
        axis_y.setRange(self.current_offset + min(siła) - 1, self.current_offset + max(siła) + 1)
        self.Graph.addAxis(axis_y, Qt.AlignLeft)
        self.series.attachAxis(axis_y)

        gui.graph_Test.setChart(self.Graph)

    #\/    v03.01.25.1
    def save_graph(self):
        sekundy = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        siła = [10, 13, 15, 18, 21, 23, 24, 25, 25, 20, 0, 0, 0]

        graph_data = {"sekundy": sekundy, "siła": siła}
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
    #/\

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