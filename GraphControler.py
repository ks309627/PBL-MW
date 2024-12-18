from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Qt
from PySide6 import QtCharts
from gui_ui import Ui_Main

class GraphControler(QMainWindow):
    def __init__(self, gui:Ui_Main):
        super().__init__()
        self.Graph = QtCharts.QChart()
        self.Graph.setTitle("Wykres siły w czasie")
        self.current_offset = 0
        self.gui = gui
        self.update_Graph(gui)


    def update_Graph(self, gui:Ui_Main):
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
        axis_y.setRange(self.current_offset + min(siła) + 1, self.current_offset + min(siła) - 1)
        self.Graph.addAxis(axis_y, Qt.AlignLeft)
        self.series.attachAxis(axis_y)

        gui.graph_Test.setChart(self.Graph)

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