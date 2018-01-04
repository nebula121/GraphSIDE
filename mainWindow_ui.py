#-------------------------------------------------------------------------------
# Name:        GraphSIDE
# Author:      nebula121 <nebula121.dev@gmail.com>
# Copyright:   (c) nebula121 2018
# Licence:     MIT License
#-------------------------------------------------------------------------------

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(292, 357)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.graphSetComboBox = QtGui.QComboBox(self.widget)
        self.graphSetComboBox.setObjectName("graphSetComboBox")
        self.verticalLayout.addWidget(self.graphSetComboBox)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.folderPathEditLayout = QtGui.QHBoxLayout()
        self.folderPathEditLayout.setObjectName("folderPathEditLayout")
        self.folderPathEdit = QtGui.QLineEdit(self.widget)
        self.folderPathEdit.setObjectName("folderPathEdit")
        self.folderPathEditLayout.addWidget(self.folderPathEdit)
        self.folderSelectDialogButton = QtGui.QPushButton(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.folderSelectDialogButton.sizePolicy().hasHeightForWidth())
        self.folderSelectDialogButton.setSizePolicy(sizePolicy)
        self.folderSelectDialogButton.setMaximumSize(QtCore.QSize(30, 16777215))
        self.folderSelectDialogButton.setObjectName("folderSelectDialogButton")
        self.folderPathEditLayout.addWidget(self.folderSelectDialogButton)
        self.formLayout.setLayout(0, QtGui.QFormLayout.FieldRole, self.folderPathEditLayout)
        self.verticalLayout.addLayout(self.formLayout)
        self.fileNameListWidget = QtGui.QListWidget(self.widget)
        self.fileNameListWidget.setObjectName("fileNameListWidget")
        self.verticalLayout.addWidget(self.fileNameListWidget)
        self.exportButton = QtGui.QPushButton(self.widget)
        self.exportButton.setObjectName("exportButton")
        self.verticalLayout.addWidget(self.exportButton)
        self.horizontalLayout.addWidget(self.widget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 292, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "ファイルの場所:", None, QtGui.QApplication.UnicodeUTF8))
        self.folderSelectDialogButton.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.exportButton.setText(QtGui.QApplication.translate("MainWindow", "一括出力", None, QtGui.QApplication.UnicodeUTF8))

