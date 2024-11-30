from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Qt
from PySide6 import QtCharts
from gui_ui import Ui_Main

class GraphControler(QMainWindow):
    def __init__(self, gui:Ui_Main):
        super().__init__()
        self.Graph = QtCharts.QChart()
        self.Graph.setTitle("Siła w Czasie")
        self.update_Graph(gui)

    def update_Graph(self, gui:Ui_Main):
        sekundy = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        siła = [10, 13, 15, 18, 21, 23, 24, 25, 25, 20, 0, 0, 0]

        self.series = QtCharts.QLineSeries()
        for i in range(len(sekundy)):
            self.series.append(i, siła[i])
        self.Graph.addSeries(self.series)

        #Add asxis and set allignemt
        axis_x = QtCharts.QBarCategoryAxis()
        axis_x.append(sekundy)
        self.Graph.addAxis(axis_x, Qt.AlignBottom)

        axis_y = QtCharts.QValueAxis()

        #Min max values
        min_y = min(sekundy)
        max_y = max(sekundy)
        axis_y.setRange(min_y, max_y)
        self.Graph.addAxis(axis_y, Qt.AllignLeft)
        
        #Attach axes to series
        self.series.attachAxis(axis_x)
        self.series.attachAxis(axis_y)

        gui.graph_Test.setChart(self.Graph)