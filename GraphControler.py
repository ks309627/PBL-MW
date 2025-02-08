from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt
from PySide6 import QtCharts
import json
import os
from gui_ui import Ui_Main
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
            self.gui = gui
            self.settings = settings
            self.folder_path = self.settings.get("graphSavePath")
            self.graph_mode = 0  # Tryb 0: Siła w czasie, Tryb 1: Siła w przemieszczeniu
            self.graph_relative_mode = 0
            self.seconds = []
            self.force = []
            self.distance = []
            self.selected_graph = 0

            # Połączenie przycisku z metodą przełączania wykresu
            self.gui.btn_Graph_mode.clicked.connect(self.change_graph_mode)
            self.gui.btn_Graph_relative.clicked.connect(self.change_graph_relative_mode)


            self.initialized = True

    def change_graph_mode(self):
        """Przełącza tryb wykresu między siłą w czasie a siłą w przemieszczeniu."""
        self.graph_mode = 1 - self.graph_mode  # Zamiana 0 ↔ 1
        self.update_graph()

    def change_graph_relative_mode(self):
        """Przełącza tryb relatywny dla osi X."""
        self.graph_relative_mode = 1 - self.graph_relative_mode  # Przełączanie między 0 i 1
        self.update_graph()
        
        if self.graph_relative_mode == 1:
            print("Tryb relatywny WŁĄCZONY")
        else:
            print("Tryb relatywny WYŁĄCZONY")


    def load_graph(self, selected_graph):
        """Ładuje dane z najnowszego pliku JSON w folderze wykresów."""
        self.selected_graph = selected_graph

        try:
            # Pobranie najnowszego folderu
            subdirectories = [os.path.join(self.folder_path, d) for d in os.listdir(self.folder_path) if os.path.isdir(os.path.join(self.folder_path, d))]
            if not subdirectories:
                self.logger.log_warning(f"Brak folderów w {self.folder_path}.")
                return

            subdirectories.sort(key=os.path.getctime, reverse=True)
            selected_subdirectory = subdirectories[self.selected_graph]

            # Znalezienie pliku JSON w folderze
            json_files = [os.path.join(selected_subdirectory, f) for f in os.listdir(selected_subdirectory) if f.endswith('.json')]
            if not json_files:
                self.logger.log_warning(f"Brak plików JSON w folderze {selected_subdirectory}.")
                return

            most_recent_file = max(json_files, key=os.path.getctime)

            # Odczytanie pliku JSON
            with open(most_recent_file, 'r') as file:
                data = json.load(file)
                self.seconds = data['seconds']
                self.force = [float(value.replace(" ", "").replace("N", "")) for value in data['force']]
                self.distance = [float(value.split(":")[-1]) for value in data['distance']]  # Pobranie wartości liczbowych

                self.update_graph()

                # Wymuszenie natychmiastowego odświeżenia wykresu
                self.gui.dsp_graph.repaint()
                self.gui.dsp_graph.update()
                self.gui.dsp_graph.setChart(self.Graph)  # Ponowne przypisanie wykresu

        except json.JSONDecodeError:
            self.logger.log_error(f"Błąd parsowania JSON w pliku {most_recent_file}.")
        except KeyError as e:
            self.logger.log_error(f"Błąd: brak klucza {e} w pliku {most_recent_file}.")

    def update_graph(self):
        """Aktualizuje wykres w zależności od trybu."""
        self.Graph.removeAllSeries()
        for axis in self.Graph.axes():
            self.Graph.removeAxis(axis)

        series = QtCharts.QLineSeries()

        if self.graph_mode == 0:
            # Wykres siły w czasie
            self.Graph.setTitle("Wykres siły w czasie")
            x_data, x_label = self.seconds, "Czas (s)"
        else:
            # Wykres siły w funkcji przemieszczenia (X maleje od lewej do prawej)
            self.Graph.setTitle("Wykres siły w przemieszczeniu")

            x_data = sorted(self.distance, reverse=True)  # Odwrócone wartości

            # if self.graph_relative_mode == 1:
            #     min_distance = x_data[-1]  # Najmniejsza wartość (koniec zakresu)
            #     x_data = [abs(val - min_distance) for val in x_data]  # Przesunięcie do 0
            #     x_data = x_data[::-1]

            # x_label = "Przemieszczenie (mm)"

            if self.graph_relative_mode == 1:
                max_distance = min(x_data)  # Maksymalna wartość przemieszczenia
                x_data = [max_distance - dist for dist in x_data]  # Przemieszczenie względem maksimum

            # Odwrócenie danych osi X: zaczynamy od największej wartości
            x_data = sorted(x_data, reverse=True)

            x_label = "Przemieszczenie (mm)"

        n = min(len(x_data), len(self.force))
        for i in range(n):
            series.append(x_data[i], self.force[i])

        self.Graph.addSeries(series)

        # Konfiguracja osi X
        axis_x = QtCharts.QValueAxis()
        axis_x.setTitleText(x_label)
        axis_x.setRange(min(x_data), max(x_data))
        axis_x.setTickCount(10)
        self.Graph.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        # Konfiguracja osi Y
        axis_y = QtCharts.QValueAxis()
        axis_y.setTitleText("Siła (N)")
        axis_y.setRange(min(self.force) - 1, max(self.force) + 1)
        self.Graph.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        self.gui.dsp_graph.setChart(self.Graph)




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


