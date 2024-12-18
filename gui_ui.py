# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCharts import QChartView
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLayout, QProgressBar, QPushButton,
    QSizePolicy, QStackedWidget, QWidget)
from icons import Icons_rc

class Ui_Main(object):
    def setupUi(self, Main):
        if not Main.objectName():
            Main.setObjectName(u"Main")
        Main.resize(1024, 600)
        Main.setMinimumSize(QSize(1024, 600))
        Main.setMaximumSize(QSize(1024, 600))
        self.Menu = QFrame(Main)
        self.Menu.setObjectName(u"Menu")
        self.Menu.setEnabled(True)
        self.Menu.setGeometry(QRect(0, 0, 1024, 75))
        self.Menu.setMinimumSize(QSize(0, 75))
        self.Menu.setMaximumSize(QSize(16777215, 75))
        self.Menu.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0.0113636 rgba(225, 225, 225, 255), stop:1 rgba(245, 245, 245, 255));")
        self.Menu.setFrameShape(QFrame.NoFrame)
        self.Menu.setFrameShadow(QFrame.Raised)
        self.horizontalLayoutWidget = QWidget(self.Menu)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(0, 0, 1031, 81))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetNoConstraint)
        self.horizontalLayout.setContentsMargins(20, 5, 20, 10)
        self.btn_Measure = QPushButton(self.horizontalLayoutWidget)
        self.btn_Measure.setObjectName(u"btn_Measure")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_Measure.sizePolicy().hasHeightForWidth())
        self.btn_Measure.setSizePolicy(sizePolicy)
        self.btn_Measure.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_Measure.setAcceptDrops(False)
        self.btn_Measure.setAutoFillBackground(False)
        self.btn_Measure.setStyleSheet(u"border-bottom-color: rgb(255, 85, 0);")
        icon = QIcon()
        icon.addFile(u":/Menu/menu/Measure.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_Measure.setIcon(icon)
        self.btn_Measure.setIconSize(QSize(48, 48))
        self.btn_Measure.setCheckable(True)
        self.btn_Measure.setChecked(True)
        self.btn_Measure.setAutoRepeat(False)
        self.btn_Measure.setAutoExclusive(True)
        self.btn_Measure.setAutoDefault(False)
        self.btn_Measure.setFlat(True)

        self.horizontalLayout.addWidget(self.btn_Measure)

        self.btn_Graphs = QPushButton(self.horizontalLayoutWidget)
        self.btn_Graphs.setObjectName(u"btn_Graphs")
        sizePolicy.setHeightForWidth(self.btn_Graphs.sizePolicy().hasHeightForWidth())
        self.btn_Graphs.setSizePolicy(sizePolicy)
        self.btn_Graphs.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_Graphs.setAcceptDrops(False)
        self.btn_Graphs.setAutoFillBackground(False)
        self.btn_Graphs.setStyleSheet(u"border-bottom-color: rgb(255, 85, 0);")
        icon1 = QIcon()
        icon1.addFile(u":/Menu/menu/Graph.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_Graphs.setIcon(icon1)
        self.btn_Graphs.setIconSize(QSize(48, 48))
        self.btn_Graphs.setCheckable(True)
        self.btn_Graphs.setChecked(False)
        self.btn_Graphs.setAutoRepeat(False)
        self.btn_Graphs.setAutoExclusive(True)
        self.btn_Graphs.setAutoDefault(False)
        self.btn_Graphs.setFlat(True)

        self.horizontalLayout.addWidget(self.btn_Graphs)

        self.btn_Settings = QPushButton(self.horizontalLayoutWidget)
        self.btn_Settings.setObjectName(u"btn_Settings")
        sizePolicy.setHeightForWidth(self.btn_Settings.sizePolicy().hasHeightForWidth())
        self.btn_Settings.setSizePolicy(sizePolicy)
        self.btn_Settings.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_Settings.setAcceptDrops(False)
        self.btn_Settings.setAutoFillBackground(False)
        self.btn_Settings.setStyleSheet(u"border-bottom-color: rgb(255, 85, 0);")
        icon2 = QIcon()
        icon2.addFile(u":/Menu/menu/Settings.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_Settings.setIcon(icon2)
        self.btn_Settings.setIconSize(QSize(48, 48))
        self.btn_Settings.setCheckable(True)
        self.btn_Settings.setChecked(False)
        self.btn_Settings.setAutoRepeat(False)
        self.btn_Settings.setAutoExclusive(True)
        self.btn_Settings.setAutoDefault(False)
        self.btn_Settings.setFlat(True)

        self.horizontalLayout.addWidget(self.btn_Settings)

        self.btn_Errors = QPushButton(self.horizontalLayoutWidget)
        self.btn_Errors.setObjectName(u"btn_Errors")
        sizePolicy.setHeightForWidth(self.btn_Errors.sizePolicy().hasHeightForWidth())
        self.btn_Errors.setSizePolicy(sizePolicy)
        self.btn_Errors.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_Errors.setAcceptDrops(False)
        self.btn_Errors.setAutoFillBackground(False)
        self.btn_Errors.setStyleSheet(u"border-bottom-color: rgb(255, 85, 0);")
        icon3 = QIcon()
        icon3.addFile(u":/Menu/menu/Error.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_Errors.setIcon(icon3)
        self.btn_Errors.setIconSize(QSize(48, 48))
        self.btn_Errors.setCheckable(True)
        self.btn_Errors.setChecked(False)
        self.btn_Errors.setAutoRepeat(False)
        self.btn_Errors.setAutoExclusive(True)
        self.btn_Errors.setAutoDefault(False)
        self.btn_Errors.setFlat(True)

        self.horizontalLayout.addWidget(self.btn_Errors)

        self.Content = QFrame(Main)
        self.Content.setObjectName(u"Content")
        self.Content.setGeometry(QRect(0, 75, 1024, 525))
        font = QFont()
        font.setFamilies([u"Futura Std Book"])
        self.Content.setFont(font)
        self.Content.setStyleSheet(u"")
        self.Content.setFrameShape(QFrame.NoFrame)
        self.Content.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.Content)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.Screen = QStackedWidget(self.Content)
        self.Screen.setObjectName(u"Screen")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.Screen.sizePolicy().hasHeightForWidth())
        self.Screen.setSizePolicy(sizePolicy1)
        self.Screen_Logo = QWidget()
        self.Screen_Logo.setObjectName(u"Screen_Logo")
        self.horizontalLayoutWidget_2 = QWidget(self.Screen_Logo)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(0, -69, 1031, 601))
        self.horizontalLayout_3 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout_3.setContentsMargins(50, 50, 50, 100)
        self.logo_Polsl = QLabel(self.horizontalLayoutWidget_2)
        self.logo_Polsl.setObjectName(u"logo_Polsl")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.logo_Polsl.sizePolicy().hasHeightForWidth())
        self.logo_Polsl.setSizePolicy(sizePolicy2)
        self.logo_Polsl.setMinimumSize(QSize(250, 250))
        self.logo_Polsl.setMaximumSize(QSize(250, 250))
        self.logo_Polsl.setBaseSize(QSize(478, 700))
        self.logo_Polsl.setPixmap(QPixmap(u":/Logo/logo/polsl.png"))
        self.logo_Polsl.setScaledContents(True)
        self.logo_Polsl.setWordWrap(False)

        self.horizontalLayout_3.addWidget(self.logo_Polsl)

        self.logoMt = QLabel(self.horizontalLayoutWidget_2)
        self.logoMt.setObjectName(u"logoMt")
        sizePolicy2.setHeightForWidth(self.logoMt.sizePolicy().hasHeightForWidth())
        self.logoMt.setSizePolicy(sizePolicy2)
        self.logoMt.setMinimumSize(QSize(250, 250))
        self.logoMt.setMaximumSize(QSize(250, 250))
        self.logoMt.setBaseSize(QSize(478, 700))
        self.logoMt.setPixmap(QPixmap(u":/Logo/logo/mt.png"))
        self.logoMt.setScaledContents(True)
        self.logoMt.setWordWrap(False)

        self.horizontalLayout_3.addWidget(self.logoMt)

        self.Screen.addWidget(self.Screen_Logo)
        self.Screen_MeasureMain = QWidget()
        self.Screen_MeasureMain.setObjectName(u"Screen_MeasureMain")
        self.title_MeasureMain = QLabel(self.Screen_MeasureMain)
        self.title_MeasureMain.setObjectName(u"title_MeasureMain")
        self.title_MeasureMain.setGeometry(QRect(50, 30, 181, 71))
        font1 = QFont()
        font1.setFamilies([u"Futura Std Book"])
        font1.setPointSize(36)
        self.title_MeasureMain.setFont(font1)
        self.title_MeasureMain.setTextFormat(Qt.AutoText)
        self.title_MeasureMain.setScaledContents(False)
        self.title_MeasureMain.setWordWrap(False)
        self.title_MeasureMain.setIndent(-1)
        self.btn_StartMeasure = QPushButton(self.Screen_MeasureMain)
        self.btn_StartMeasure.setObjectName(u"btn_StartMeasure")
        self.btn_StartMeasure.setGeometry(QRect(360, 210, 281, 91))
        font2 = QFont()
        font2.setFamilies([u"Futura Std Book"])
        font2.setPointSize(24)
        self.btn_StartMeasure.setFont(font2)
        self.btn_StartMeasure.setStyleSheet(u"background-color: rgb(191, 191, 191);")
        self.btn_MeasureToGraph = QPushButton(self.Screen_MeasureMain)
        self.btn_MeasureToGraph.setObjectName(u"btn_MeasureToGraph")
        self.btn_MeasureToGraph.setGeometry(QRect(250, 320, 531, 91))
        self.btn_MeasureToGraph.setFont(font2)
        self.btn_MeasureToGraph.setAutoFillBackground(False)
        self.btn_MeasureToGraph.setStyleSheet(u"background-color: rgb(191, 191, 191);")
        self.btn_MeasureToGraph.setAutoRepeat(False)
        self.Screen.addWidget(self.Screen_MeasureMain)
        self.Screen_MeasureProgress = QWidget()
        self.Screen_MeasureProgress.setObjectName(u"Screen_MeasureProgress")
        self.title_MeasureProgress = QLabel(self.Screen_MeasureProgress)
        self.title_MeasureProgress.setObjectName(u"title_MeasureProgress")
        self.title_MeasureProgress.setGeometry(QRect(70, 50, 491, 71))
        self.title_MeasureProgress.setFont(font1)
        self.title_MeasureProgress.setTextFormat(Qt.AutoText)
        self.title_MeasureProgress.setScaledContents(False)
        self.title_MeasureProgress.setWordWrap(False)
        self.title_MeasureProgress.setIndent(-1)
        self.progressBar = QProgressBar(self.Screen_MeasureProgress)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(40, 140, 921, 16))
        font3 = QFont()
        font3.setFamilies([u"Arial"])
        self.progressBar.setFont(font3)
        self.progressBar.setValue(24)
        self.progressBar.setTextVisible(False)
        self.progressBar.setInvertedAppearance(False)
        self.btn_StopMeasure = QPushButton(self.Screen_MeasureProgress)
        self.btn_StopMeasure.setObjectName(u"btn_StopMeasure")
        self.btn_StopMeasure.setGeometry(QRect(680, 180, 281, 91))
        self.btn_StopMeasure.setFont(font2)
        self.btn_StopMeasure.setStyleSheet(u"background-color: rgb(191, 191, 191);")
        self.pushButton = QPushButton(self.Screen_MeasureProgress)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(70, 280, 201, 191))
        font4 = QFont()
        font4.setFamilies([u"Futura Std Book"])
        font4.setPointSize(20)
        self.pushButton.setFont(font4)
        self.pushButton_2 = QPushButton(self.Screen_MeasureProgress)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(310, 280, 201, 191))
        self.pushButton_2.setFont(font4)
        self.title_MeasureProgress_2 = QLabel(self.Screen_MeasureProgress)
        self.title_MeasureProgress_2.setObjectName(u"title_MeasureProgress_2")
        self.title_MeasureProgress_2.setGeometry(QRect(40, 190, 491, 71))
        self.title_MeasureProgress_2.setFont(font1)
        self.title_MeasureProgress_2.setTextFormat(Qt.AutoText)
        self.title_MeasureProgress_2.setScaledContents(False)
        self.title_MeasureProgress_2.setWordWrap(False)
        self.title_MeasureProgress_2.setIndent(-1)
        self.pushButton_3 = QPushButton(self.Screen_MeasureProgress)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(570, 440, 91, 31))
        self.labelConnectionStatus = QLabel(self.Screen_MeasureProgress)
        self.labelConnectionStatus.setObjectName(u"labelConnectionStatus")
        self.labelConnectionStatus.setGeometry(QRect(590, 400, 47, 13))
        self.Screen.addWidget(self.Screen_MeasureProgress)
        self.Screen_Graphs = QWidget()
        self.Screen_Graphs.setObjectName(u"Screen_Graphs")
        self.title_Graphs = QLabel(self.Screen_Graphs)
        self.title_Graphs.setObjectName(u"title_Graphs")
        self.title_Graphs.setGeometry(QRect(60, 40, 491, 71))
        self.title_Graphs.setFont(font1)
        self.title_Graphs.setTextFormat(Qt.AutoText)
        self.title_Graphs.setScaledContents(False)
        self.title_Graphs.setWordWrap(False)
        self.title_Graphs.setIndent(-1)
        self.graph_Test = QChartView(self.Screen_Graphs)
        self.graph_Test.setObjectName(u"graph_Test")
        self.graph_Test.setGeometry(QRect(90, 130, 701, 341))
        self.gridLayoutWidget = QWidget(self.Screen_Graphs)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(798, 210, 239, 141))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.btn_Graph_up = QPushButton(self.gridLayoutWidget)
        self.btn_Graph_up.setObjectName(u"btn_Graph_up")

        self.gridLayout.addWidget(self.btn_Graph_up, 0, 1, 1, 1)

        self.btn_Graph_down = QPushButton(self.gridLayoutWidget)
        self.btn_Graph_down.setObjectName(u"btn_Graph_down")

        self.gridLayout.addWidget(self.btn_Graph_down, 1, 1, 1, 1)

        self.btn_Graph_left = QPushButton(self.gridLayoutWidget)
        self.btn_Graph_left.setObjectName(u"btn_Graph_left")

        self.gridLayout.addWidget(self.btn_Graph_left, 1, 0, 1, 1)

        self.btn_Graph_right = QPushButton(self.gridLayoutWidget)
        self.btn_Graph_right.setObjectName(u"btn_Graph_right")

        self.gridLayout.addWidget(self.btn_Graph_right, 1, 2, 1, 1)

        self.btn_Graph_zout = QPushButton(self.gridLayoutWidget)
        self.btn_Graph_zout.setObjectName(u"btn_Graph_zout")

        self.gridLayout.addWidget(self.btn_Graph_zout, 0, 0, 1, 1)

        self.btn_Graph_zin = QPushButton(self.gridLayoutWidget)
        self.btn_Graph_zin.setObjectName(u"btn_Graph_zin")

        self.gridLayout.addWidget(self.btn_Graph_zin, 0, 2, 1, 1)

        self.btn_Graph_resetview = QPushButton(self.gridLayoutWidget)
        self.btn_Graph_resetview.setObjectName(u"btn_Graph_resetview")

        self.gridLayout.addWidget(self.btn_Graph_resetview, 2, 1, 1, 1)

        self.Screen.addWidget(self.Screen_Graphs)
        self.Screen_Settings = QWidget()
        self.Screen_Settings.setObjectName(u"Screen_Settings")
        self.title_Settings = QLabel(self.Screen_Settings)
        self.title_Settings.setObjectName(u"title_Settings")
        self.title_Settings.setGeometry(QRect(100, 50, 491, 71))
        self.title_Settings.setFont(font1)
        self.title_Settings.setTextFormat(Qt.AutoText)
        self.title_Settings.setScaledContents(False)
        self.title_Settings.setWordWrap(False)
        self.title_Settings.setIndent(-1)
        self.Screen.addWidget(self.Screen_Settings)
        self.Screen_Errors = QWidget()
        self.Screen_Errors.setObjectName(u"Screen_Errors")
        self.title_Errors = QLabel(self.Screen_Errors)
        self.title_Errors.setObjectName(u"title_Errors")
        self.title_Errors.setGeometry(QRect(60, 50, 491, 71))
        self.title_Errors.setFont(font1)
        self.title_Errors.setTextFormat(Qt.AutoText)
        self.title_Errors.setScaledContents(False)
        self.title_Errors.setWordWrap(False)
        self.title_Errors.setIndent(-1)
        self.Screen.addWidget(self.Screen_Errors)

        self.horizontalLayout_2.addWidget(self.Screen)


        self.retranslateUi(Main)

        self.btn_Measure.setDefault(False)
        self.btn_Graphs.setDefault(False)
        self.btn_Settings.setDefault(False)
        self.btn_Errors.setDefault(False)
        self.Screen.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(Main)
    # setupUi

    def retranslateUi(self, Main):
        Main.setWindowTitle(QCoreApplication.translate("Main", u"Form", None))
        self.btn_Measure.setText("")
        self.btn_Graphs.setText("")
        self.btn_Settings.setText("")
        self.btn_Errors.setText("")
        self.logo_Polsl.setText("")
        self.logoMt.setText("")
        self.title_MeasureMain.setText(QCoreApplication.translate("Main", u"Pomiary", None))
        self.btn_StartMeasure.setText(QCoreApplication.translate("Main", u"Wykonaj Pomiar", None))
        self.btn_MeasureToGraph.setText(QCoreApplication.translate("Main", u"Przejd\u017a do poprzedniego Pomiaru", None))
        self.title_MeasureProgress.setText(QCoreApplication.translate("Main", u"Wykonywanie Pomiaru", None))
        self.btn_StopMeasure.setText(QCoreApplication.translate("Main", u"Zatrzymaj", None))
        self.pushButton.setText(QCoreApplication.translate("Main", u"Obr\u00f3t w Lewo", None))
        self.pushButton_2.setText(QCoreApplication.translate("Main", u"Obr\u00f3t w Prawo", None))
        self.title_MeasureProgress_2.setText(QCoreApplication.translate("Main", u"Tymczasowo do test\u00f3w:", None))
        self.pushButton_3.setText(QCoreApplication.translate("Main", u"Refresh", None))
        self.labelConnectionStatus.setText(QCoreApplication.translate("Main", u"TextLabel", None))
        self.title_Graphs.setText(QCoreApplication.translate("Main", u"Wykresy", None))
        self.btn_Graph_up.setText(QCoreApplication.translate("Main", u"G\u00f3ra", None))
        self.btn_Graph_down.setText(QCoreApplication.translate("Main", u"D\u00f3\u0142", None))
        self.btn_Graph_left.setText(QCoreApplication.translate("Main", u"Lewo", None))
        self.btn_Graph_right.setText(QCoreApplication.translate("Main", u"Prawo", None))
        self.btn_Graph_zout.setText(QCoreApplication.translate("Main", u"Zoom out", None))
        self.btn_Graph_zin.setText(QCoreApplication.translate("Main", u"Zoom in", None))
        self.btn_Graph_resetview.setText(QCoreApplication.translate("Main", u"Graph Reset", None))
        self.title_Settings.setText(QCoreApplication.translate("Main", u"Ustawienia", None))
        self.title_Errors.setText(QCoreApplication.translate("Main", u"B\u0142\u0119dy", None))
    # retranslateUi

