# import pdb; pdb.set_trace()
#-------------------------------------------------------------------------------
# Name:        GraphSIDE
# Version:     0.1.0
# Purpose:     Make multi-axis Graphs from data file
#
# Author:      nebula121 <nebula121.dev@gmail.com>
#
# LastUpdate:  2018/01/03
# Created:     2015/07/11
# Copyright:   (c) nebula121 2018
# Licence:     MIT License
#-------------------------------------------------------------------------------

import sys
import os
import numpy as np
import pandas as pd
from PySide.QtCore import *
from PySide.QtGui import *
#from PySide.QtUiTools import QUiLoader
from mainWindow_ui import Ui_MainWindow
import pyqtgraph as pg
import pyqtgraph.exporters
import json
#import codecs
from settingDialog import SettingDialog
from graphSetViewWidget import GraphSetViewWidget
from setting import Setting
import gc

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # ウィンドウタイトルを設定
        self.setWindowTitle('GraphSIDE')

        # 設定ファイルを読み込みむ
        self.loadSettings()

        print('GUI create')

        # GUI部品を作成
        #self.ui = QUiLoader().load("./mainWindow.ui")
        self.ui = self
        # self.imageScaleCheckBox = QCheckBox()

        # GUI部品の設定を修正
        self.setupUi(self)
        self.setupUi2()
        
        print('GUI created')

        # 保持する変数を宣言
        self.tempFolderPath = ""    # ファイルリスト用
        self.tempFolderPath2 = ""   # グラフ出力用
        self.tempFileList = []

        # シグナルスロット接続
        print('SIGNAL SLOT connect')

        self.ui.graphSetComboBox.currentIndexChanged.connect(lambda: self.setCurrentSetting(self.ui.graphSetComboBox.currentIndex() + 1))
        self.ui.folderPathEdit.textChanged.connect(lambda: self.checkFolderPathEditError(self.ui.folderPathEdit.text()))
        self.ui.folderPathEdit.textChanged.connect(lambda: self.updateFileNameListWidget(self.ui.folderPathEdit.text()))
        self.ui.fileNameListWidget.itemClicked.connect(lambda: self.createGraph(self.settings["general"], 
                                                                             self.currentDataSetSetting, 
                                                                             self.currentGraphSetSetting, 
                                                                             self.tempFolderPath, 
                                                                             self.ui.fileNameListWidget.selectedItems()[0].text()))
        # self.imageScaleCheckBox.stateChanged.connect(lambda: self.changeImageScale(self.imageScaleCheckBox.isChecked()))
        self.ui.exportButton.clicked.connect(lambda: self.exportGraphsByFile(self.ui.fileNameListWidget.selectedItems()))
        #self.ui.settingButton.clicked.connect(lambda: self.openSettingDialog(self.settings["dataSet"], self.settings["graphSet"]))
        self.ui.folderSelectDialogButton.clicked.connect(lambda: self.openFolderSelectDialog(self.ui.folderPathEdit.text()))

        print('SIGNAL SLOT connected')

        # 起動時処理
        self.checkFolderPathEditError(self.ui.folderPathEdit.text())
        self.updateFileNameListWidget(self.ui.folderPathEdit.text())
        # self.changeImageScale(self.imageScaleCheckBox.isChecked())
        self.imageScale = 1 # 仮
        self.setCurrentSetting(self.ui.graphSetComboBox.currentIndex() + 1)

        # フォルダ内変更を即時反映
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.updateFileNameListWidget(self.tempFolderPath))
        self.timer.start(1000)


    def setupUi2(self):
        graphSetTitleList = list()
        i = 0

        while i < len(self.settings["graphSet"].keys()):
            graphSetTitleList.append(self.settings["graphSet"]["graphSet" + str(i + 1)]["title"])
            i += 1
        self.ui.graphSetComboBox.addItems(graphSetTitleList)
        index = self.settings["lastState"]["graphSet"]["index"]
        if index < self.ui.graphSetComboBox.count():
            self.ui.graphSetComboBox.setCurrentIndex(index - 1)

        self.ui.folderPathEdit.setText(self.settings["lastState"]["dir"])

        self.ui.folderSelectDialogButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.ui.folderSelectDialogButton.setMaximumWidth(30)

        self.ui.fileNameListWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.ui.exportButton.setEnabled(False)

        self.ui.statusbar.setHidden(True)
     
        menu1 = QMenu("&File")
        act1_1 = QAction("設定", self)
        act1_2 = QAction("終了", self)
        act1_1.triggered.connect(lambda: self.openSettingDialog(self.settings["dataSet"], self.settings["graphSet"]))
        act1_2.triggered.connect(lambda: self.close())
        menu1.addAction(act1_1)
        menu1.addAction(act1_2)
        
        menu2 = QMenu("&Help")
        act2_1 = QAction("&About GraphSIDE", self)
        act2_1.triggered.connect(lambda: self.openAboutDialog())
        menu2.addAction(act2_1)

        self.ui.menubar.addMenu(menu1)
        self.ui.menubar.addMenu(menu2)


    def setCurrentSetting(self, graphSetIndex):
        if graphSetIndex is 0:
            return

        graphSetStrIndex = "graphSet" + str(graphSetIndex)

        self.currentGraphSetSetting = self.settings["graphSet"][graphSetStrIndex]
        self.currentDataSetSetting = self.settings["dataSet"]["dataSet" + str(self.currentGraphSetSetting["dataSet"]["index"])]


    def checkFolderPathEditError(self, folderPath):
        if os.path.exists(str(folderPath)):
            self.tempFolderPath = folderPath
            self.ui.folderPathEdit.setStyleSheet("background-color:white")
        else:
            self.ui.folderPathEdit.setStyleSheet("background-color:rgba(255,150,150,255)")


    def updateFileNameListWidget(self, folderPath):
        if folderPath in self.settings["shortcut"]:
            self.ui.folderPathEdit.setText(self.settings["shortcut"][folderPath])
            return

        if os.path.exists(str(folderPath)):
            if os.listdir(folderPath) != self.tempFileList:
                self.ui.fileNameListWidget.clear()
                self.ui.fileNameListWidget.addItems(os.listdir(folderPath))

                self.tempFileList = os.listdir(folderPath)


    def updateGraphSetComboBox(self):
        oldGraphSetTitle = self.ui.graphSetComboBox.currentText()
        self.ui.graphSetComboBox.clear()
        
        graphSetTitleList = list()
        i = 0
        
        while i < len(self.settings["graphSet"].keys()):
            graphSetTitleList.append(self.settings["graphSet"]["graphSet" + str(i + 1)]["title"])
            i += 1
        self.ui.graphSetComboBox.addItems(graphSetTitleList)
        index = self.ui.graphSetComboBox.findText(oldGraphSetTitle)
        self.ui.graphSetComboBox.setCurrentIndex(index)


    #def changeImageScale(self, checkState):
    #    if checkState == False:
    #        self.imageScale = 1
    #    elif checkState == True:
    #        self.imageScale = 4


    def createGraph(self, generalSetting, dataSetSetting, graphSetSetting, folderPath, fileName):
        # [6-1] データリスト一式を生成
        try:
            self.createGraphErrorMsg = str("ファイル、または、データの読み込みに失敗しました。")
            dataSet = self.loadDataSet(dataSetSetting, folderPath, fileName)
            self.createGraphErrorMsg = str("Raw dataの加工(係数の乗算)に失敗しました。\n\n" + 
                                           
                                           "  1. Graph setとデータファイルの対応を確認してください。\n" + 
                                           "  2. 設定 > Data set > Raw dataとデータファイルの系列の対応を確認してください。\n" + 
                                           "      使用しないデータ系列(文字列の場合など)の係数は0にしてください。")
            dataSet = self.processDataSet(dataSet)
            self.createGraphErrorMsg = str("Calc dataの生成に失敗しました。\n\n" + 
                                           
                                           "  1. 設定 > Data set > Calc dataの設定を確認してください。")
            dataSet = self.createCalcDataSet(dataSet)
            self.createGraphErrorMsg = str("グラフの描写に失敗しました。")
            self.createGraphSetViewWindow(generalSetting, graphSetSetting, dataSetSetting, dataSet)
            
            self.createGraphErrorMsg = str("")
        except:
            ErrorMB = QMessageBox()
            ErrorMB.setText(self.createGraphErrorMsg)
            ErrorMB.setIcon(QMessageBox.Warning)
            ErrorMB.exec_()
            return()
                
        self.ui.setWindowTitle('GraphSIDE - ' + fileName)


    def loadDataSet(self, dataSetSetting, folderPath, fileName):
        filePath = folderPath + "//" + fileName
        dataSet = np.loadtxt(filePath, delimiter=",", skiprows=dataSetSetting["headerNum"]).T
        indexData = np.arange(dataSet.shape[1])
        constData = np.ones(dataSet.shape[1])
        dataSet = np.vstack([indexData, constData, dataSet])

        return dataSet
    

    def processDataSet(self, dataSet):
        rawDataSetSettings = self.currentDataSetSetting["rawData"]
        loopNum = 2

        for rawDataSetSettingStrIndex, rawData in zip(sorted(rawDataSetSettings), dataSet[2:]):
            rawDataSetSetting = rawDataSetSettings[rawDataSetSettingStrIndex]

            if rawDataSetSetting["coefficient"] is not (0 or 1):
                dataSet[loopNum] = rawDataSetSetting["coefficient"] * rawData
            
            loopNum += 1

        return dataSet


    def createCalcDataSet(self, dataSet):
        calcDataSettings = self.currentDataSetSetting["calcData"]
        
        i = 1

        while i <= len(calcDataSettings):
            calcData = np.array
            
            firstCoefficient = calcDataSettings["calcData" + str(i)]["firstCoefficient"]
            firstData = np.array(dataSet[self.getDataIndex(calcDataSettings["calcData" + str(i)]["firstData"])])
            secondCoefficient = calcDataSettings["calcData" + str(i)]["secondCoefficient"]
            secondData = np.array(dataSet[self.getDataIndex(calcDataSettings["calcData" + str(i)]["secondData"])])

            if calcDataSettings["calcData" + str(i)]["operator"] == "+":
                calcData = firstCoefficient * firstData + secondCoefficient * secondData
            elif calcDataSettings["calcData" + str(i)]["operator"] == "-":
                calcData = firstCoefficient * firstData - secondCoefficient * secondData
            elif calcDataSettings["calcData" + str(i)]["operator"] == "":
                calcData = firstCoefficient * firstData
            print(calcData)
            dataSet = np.vstack([dataSet, calcData])

            i += 1

        return dataSet


    def getDataIndex(self, dataProperty):
        defaultDataNum = 2
        rawDataNum = len(self.currentDataSetSetting["rawData"])
        calcDataNum = len(self.currentDataSetSetting["calcData"])
        
        if dataProperty[0] == "d":
            return int(dataProperty[1:]) - 1
        elif dataProperty[0] == "r":
            return defaultDataNum + int(dataProperty[1:]) - 1
        elif dataProperty[0] == "c":
            return defaultDataNum + rawDataNum + int(dataProperty[1:]) - 1


    def createGraphSetViewWindow(self, generalSetting, graphSetSetting, dataSetSetting, dataSet):
        if hasattr(self, "graphWidget"):
            self.graphWidget.deleteLater()
            gc.collect()
        
        self.graphWidget = GraphSetViewWidget(generalSetting = generalSetting, graphSetSetting = graphSetSetting, dataSetSetting = dataSetSetting, dataSet = dataSet, imageScale = self.imageScale)
        self.ui.horizontalLayout.addWidget(self.graphWidget)

        self.ui.exportButton.setEnabled(True)
        self.tempFolderPath2 = self.tempFolderPath

        #self.graphWin = GraphSetViewWidget(graphSetSetting = graphSetSetting,
        #dataSet = dataSet, imageScale = self.imageScale)
        #mainWinX = self.x()
        #mainWinY = self.y()
        #mainWinW = self.frameGeometry().width()
        #self.graphWin.move(mainWinX + mainWinW, mainWinY)
        #self.graphWin.show()
        #self.graphWin.setWindowTitle('グラフ出力 - ' +
        #self.ui.fileNameListWidget.selectedItems()[0].text())


    def loadSettings(self):
        qDebug("load settings")
        
        try:
            os.path.exists(".\\settings.json")
            self.settingsClass = Setting(filePath = ".\\settings.json")
        except:
            self.settingsClass = Setting()
            
            ErrorMB = QMessageBox()
            ErrorMB.setText("設定ファイルが確認されなかったため\n初期化された設定を読み込みました")
            ErrorMB.setIcon(QMessageBox.Information)
            ErrorMB.exec_()

        self.settings = self.settingsClass.settings

        qDebug("loaded")


    def saveSettings(self):
        self.settings["lastState"]["dir"] = self.ui.folderPathEdit.text()
        self.settings["lastState"]["graphSet"]["index"] = self.ui.graphSetComboBox.currentIndex() + 1
        self.settings["lastState"]["graphSet"]["id"] = self.settings["graphSet"]["graphSet" + str(self.ui.graphSetComboBox.currentIndex() + 1)]["id"]
        geometry = str(self.ui.geometry()).replace("PySide.QtCore.QRect(", "").replace(")", "")
        self.settings["lastState"]["geometry"] = geometry

        self.settings = {
                    "general": self.settings["general"],
                    "lastState": self.settings["lastState"],
                    "dataSet": self.settings["dataSet"],
                    "graphSet": self.settings["graphSet"],
                    "shortcut": self.settings["shortcut"]
                    }

        self.settingsClass.save(filePath = ".\\settings.json", settings = self.settings)


    def openSettingDialog(self, dataSetSettings, graphSetSettings):
        if hasattr(self, "dialog"):
            self.dialog.ui.activateWindow()
            return
        
        self.dialog = SettingDialog(settings = self.settings)
        self.dialog.ui.show()

        QObject.connect(self.dialog.ui, SIGNAL('accepted()'), self.settingDialogAccepted)
        QObject.connect(self.dialog.ui, SIGNAL('rejected()'), self.settingDialogRejected)
        QObject.connect(self.dialog.ui.allowButton, SIGNAL('clicked()'), self.settingDialogAllowed)


    def settingDialogAccepted(self):
        qDebug("accepted")
        self.dialog.updateTempSetting(self.dialog.ui.treeWidget.currentItem())
        self.settings = self.dialog.tempSettings
        self.setCurrentSetting(self.ui.graphSetComboBox.currentIndex() + 1)
        self.disconnectSettingDialog()
        self.dialog.deleteLater()
        del self.dialog

        self.updateGraphSetComboBox()


    def settingDialogRejected(self):
        qDebug("rejected")
        self.disconnectSettingDialog()
        self.dialog.deleteLater()
        del self.dialog


    def settingDialogAllowed(self):
        qDebug("allowed")
        self.dialog.updateTempSetting(self.dialog.ui.treeWidget.currentItem())
        self.settings = self.dialog.tempSettings
        self.setCurrentSetting(self.ui.graphSetComboBox.currentIndex() + 1)


    def disconnectSettingDialog(self):
        QObject.disconnect(self.dialog.ui, SIGNAL('accepted()'), self.settingDialogAccepted)
        QObject.disconnect(self.dialog.ui, SIGNAL('rejected()'), self.settingDialogRejected)
        QObject.disconnect(self.dialog.ui.allowButton, SIGNAL('clicked()'), self.settingDialogAllowed)
        

    def openFolderSelectDialog(self, dir):
        dialog = QFileDialog(directory = dir)
        dialog.setFileMode(QFileDialog.Directory);
        dialog.setOption(QFileDialog.ShowDirsOnly, True);
        if dialog.exec():
            folderPath = dialog.selectedFiles()[0]
            folderPath = folderPath.replace('/', '\\')
            self.ui.folderPathEdit.setText(folderPath)


    def openAboutDialog(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("About GraphSIDE")
        msgBox.setTextFormat(Qt.RichText)
        msgBox.setText("GraphSIDE Ver. 0.1.0 (2016/10/25)<br><br>" + 
                       "Copyright&copy;  2016 nebula121 (nebula121.dev@gmail.com)<br>" + 
                       "<a href = https://sites.google.com/site/nebula121dev/graphside>https://sites.google.com/site/nebula121dev/graphside</a>"
                       )
        msgBox.exec_()
    
    
    def exportGraphsByFile(self, fileNameList=list()):
        if os.path.exists(self.tempFolderPath2 + "\\exportGraphs") == False :
            createExportFolderMsgBox = QMessageBox()
            createExportFolderMsgBox.setText("出力先フォルダが存在しません。\n新規作成しますか？")
            createExportFolderMsgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
            createExportFolderMsgBox.setDefaultButton(QMessageBox.Yes)
            createExportFolderMsgBox.setIcon(QMessageBox.Question)
            ret = createExportFolderMsgBox.exec_()

            if ret == QMessageBox.Yes:
                os.mkdir(self.tempFolderPath2 + "\\exportGraphs")
            elif ret == QMessageBox.Cancel:
                return

        if len(fileNameList) == 0:
            self.exportGraphs(self.graphWidget.pIList)
        else:
            for fileName in fileNameList:
                self.createGraph(self.settings["general"], 
                                 self.currentDataSetSetting, 
                                 self.currentGraphSetSetting, 
                                 self.tempFolderPath, 
                                 fileName.text())

                self.exportGraphs(self.graphWidget.pIList)


    def exportGraphs(self, pIList=list()):
        if len(pIList) == 0:
            return
        
        i = 0
        yesToAllFlag = False
        noToAllFlag = False

        while i < len(pIList):
            if os.path.exists(self.tempFolderPath2 + "\\exportGraphs\\" + self.windowTitle() + "_" + str(i + 1) + ".png") == False:
                while (pIList[i][0].width() == 640) & (pIList[i][0].height() == 480):
                   delayMB = QMessageBox()
                   delayMB.setText("Delay...")
                   delaytimer = QTimer()
                   delaytimer.timeout.connect(lambda: delayMB.close())
                   delaytimer.start(100)
                   delayMB.exec_()

                exporter = pg.exporters.ImageExporter(pIList[i][0])
                exporter.parameters()['width'] = self.imageScale * pIList[i][0].width()
            
                exporter.export(self.tempFolderPath2 + "\\exportGraphs\\" + self.windowTitle() + "_" + str(i + 1) + ".png")

            elif os.path.exists(self.tempFolderPath2 + "\\exportGraphs\\" + self.windowTitle() + "_" + str(i + 1) + ".png") == True:
                if (yesToAllFlag | noToAllFlag) == False:
                    graphImageExistErrorMsgBox = QMessageBox()
                    graphImageExistErrorMsgBox.setText(self.windowTitle() + "_" + str(i + 1) + ".png" + "が存在します。\n上書きしますか？")
                    graphImageExistErrorMsgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.YesToAll | QMessageBox.No | QMessageBox.NoToAll)
                    graphImageExistErrorMsgBox.setDefaultButton(QMessageBox.Yes)
                    graphImageExistErrorMsgBox.setIcon(QMessageBox.Question)
                    ret = graphImageExistErrorMsgBox.exec_()

                    if ret == QMessageBox.Yes:
                        pass

                    elif ret == QMessageBox.YesToAll:
                        yesToAllFlag = True

                    elif ret == QMessageBox.No:
                        i += 1
                        continue

                    elif ret == QMessageBox.NoToAll:
                        noToAllFlag = True
                        i += 1
                        continue
                    
                    while (pIList[i][0].width() == 640) & (pIList[i][0].height() == 480):
                       delayMB = QMessageBox()
                       delayMB.setText("Delay...")
                       delaytimer = QTimer()
                       delaytimer.timeout.connect(lambda: delayMB.close())
                       delaytimer.start(100)
                       delayMB.exec_()

                    exporter = pg.exporters.ImageExporter(pIList[i][0])
                    exporter.parameters()['width'] = self.imageScale * pIList[i][0].width()
                        
                    exporter.export(self.tempFolderPath2 + "\\exportGraphs\\" + self.windowTitle() + "_" + str(i + 1) + ".png")

                elif yesToAllFlag == True:
                    exporter = pg.exporters.ImageExporter(pIList[i][0])
                    exporter.parameters()['width'] = self.imageScale * pIList[i][0].width()
                    
                    exporter.export(self.tempFolderPath2 + "\\exportGraphs\\" + self.windowTitle() + "_" + str(i + 1) + ".png")

                elif noToAllFlag == True:
                    pass
            
            i += 1

    def closeEvent(self, event):
        self.saveSettings()#settings.setValue("geometry", saveGeometry());
        self.ui.close()
        #QMainWindow.closeEvent(event);


if __name__ == '__main__':
    # Qt Applicationを作ります
    app = QApplication(sys.argv)
    # formを作成して表示します
    mainWin = MainWindow()
    mainWin.ui.show()
    # Qtのメインループを開始します
    sys.exit(app.exec_())
