# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'testgui.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLineEdit, QPushButton, QSizePolicy,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(491, 753)
        self.verticalLayoutWidget = QWidget(Form)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 513, 751))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.Input = QLineEdit(self.verticalLayoutWidget)
        self.Input.setObjectName(u"Input")
        font = QFont()
        font.setFamilies([u"Comic Sans MS"])
        font.setPointSize(36)
        self.Input.setFont(font)

        self.verticalLayout.addWidget(self.Input)

        self.Button = QPushButton(self.verticalLayoutWidget)
        self.Button.setObjectName(u"Button")
        font1 = QFont()
        font1.setFamilies([u"Comic Sans MS"])
        font1.setPointSize(72)
        self.Button.setFont(font1)

        self.verticalLayout.addWidget(self.Button)

        self.Output = QTextEdit(self.verticalLayoutWidget)
        self.Output.setObjectName(u"Output")
        font2 = QFont()
        font2.setPointSize(20)
        self.Output.setFont(font2)

        self.verticalLayout.addWidget(self.Output)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.Button.setText(QCoreApplication.translate("Form", u"PushButton", None))
    # retranslateUi

