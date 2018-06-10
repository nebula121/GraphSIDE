#-------------------------------------------------------------------------------
# Name:        GraphSIDE
# Author:      nebula121 <nebula121.dev@gmail.com>
# Copyright:   (c) nebula121 2018
# Licence:     MIT License
#-------------------------------------------------------------------------------

import sys
from PySide.QtCore import *
from PySide.QtGui import *
import pyqtgraph as pg
from setting import Setting

class PlotSetting(QDialog):
    plotSettingChanged = Signal()
    
    def __init__(self, parent = None, plotSettingWidgetUi = None, graphPropertyItem = None, dataSetSetting = {}):
        super(PlotSetting, self).__init__(parent)
        
        self.tempDataSetSetting = dataSetSetting
        self.ui = plotSettingWidgetUi
        self.setupUi()

        self.ui.plotTreeWidget.currentItemChanged.connect(lambda: self.setupUiPlotDetail(self.ui.plotTreeWidget.currentItem()))

        self.slot1 = lambda: self.updatePlotPropertyItem(title = "", color = self.ui.plotColorEdit.text(), 
                                                         dataScopeMax = self.ui.dataScopeSpinBox1.value(), dataScopeMin = self.ui.dataScopeSpinBox2.value(), 
                                                         x = self.getDataIdFromIndex(self.ui.xComboBox.currentIndex()), y = self.getDataIdFromIndex(self.ui.yComboBox.currentIndex()), 
                                                         yAxis = self.ui.yAxisComboBox.currentIndex(), style = self.ui.styleComboBox.currentText())
        self.ui.styleComboBox.currentIndexChanged.connect(self.slot1)
        self.ui.plotColorEdit.textChanged.connect(self.slot1)
        self.ui.xComboBox.currentIndexChanged.connect(self.slot1)
        self.ui.yComboBox.currentIndexChanged.connect(self.slot1)
        self.ui.dataScopeSpinBox1.valueChanged.connect(self.slot1)
        self.ui.dataScopeSpinBox2.valueChanged.connect(self.slot1)
        self.ui.yAxisComboBox.currentIndexChanged.connect(self.slot1)

        #self.ui.plotColorEdit.textChanged.connect(lambda: self.checkColorPathEditError(color = self.ui.plotColorEdit.text()))

        self.ui.plotNewButton.clicked.connect(lambda: self.insertTreeWidgetItem(treeWidget = self.ui.plotTreeWidget, 
                                                                                index = self.ui.plotTreeWidget.indexOfTopLevelItem(self.ui.plotTreeWidget.currentItem())))
        self.ui.plotCopyButton.clicked.connect(lambda: self.insertTreeWidgetItem(treeWidget = self.ui.plotTreeWidget, 
                                                                                 index = self.ui.plotTreeWidget.indexOfTopLevelItem(self.ui.plotTreeWidget.currentItem()), 
                                                                                 item = self.ui.plotTreeWidget.currentItem().clone()))
        self.ui.plotUpButton.clicked.connect(lambda: self.moveTreeWidgetItem(treeWidget = self.ui.plotTreeWidget, 
                                                                                index = self.ui.plotTreeWidget.indexOfTopLevelItem(self.ui.plotTreeWidget.currentItem()), 
                                                                                direction = -1))
        self.ui.plotDownButton.clicked.connect(lambda: self.moveTreeWidgetItem(treeWidget = self.ui.plotTreeWidget, 
                                                                                index = self.ui.plotTreeWidget.indexOfTopLevelItem(self.ui.plotTreeWidget.currentItem()), 
                                                                                direction = +1))
        self.ui.plotDeleteButton.clicked.connect(lambda: self.deleteTreeWidgetItem(treeWidget = self.ui.plotTreeWidget, 
                                                                                   index = self.ui.plotTreeWidget.indexOfTopLevelItem(self.ui.plotTreeWidget.currentItem())))


    def setupUi(self):
        self.ui.plotTreeWidget.setHeaderLabels(["title", "Color", "dataScopeMax", "dataScopeMin", "x", "y", "yAxis", "Style", "X", "Y", "Axis"])

        self.ui.plotTreeWidget.setColumnHidden(0, True)
        self.ui.plotTreeWidget.setColumnHidden(2, True)
        self.ui.plotTreeWidget.setColumnHidden(3, True)
        self.ui.plotTreeWidget.setColumnHidden(4, True)
        self.ui.plotTreeWidget.setColumnHidden(5, True)
        self.ui.plotTreeWidget.setColumnHidden(6, True)

        header = self.ui.plotTreeWidget.header()
        header.moveSection(1, 0) # "Color" -> 1
        header.moveSection(7, 0) # "Style" -> 0
        header.moveSection(8, 2) # "X" -> 2
        header.moveSection(9, 3) # "Y" -> 3
        header.moveSection(10, 4) # "Axis" -> 4

        self.ui.styleComboBox.addItems(["Line (Solid)", "Line (Dash)", "Line (Dot)", "Line (DashDot)", "Line (DashDotDot)", 
                                     "Point (Circle)", "Point (Square)", "Point (Triangle)", "Point (Diamond)", "Point (Plus)"])

        dataNameList = self.getDataNameList2()
        
        self.ui.xComboBox.addItems(dataNameList)
        self.ui.yComboBox.addItems(dataNameList)
        
        self.ui.dataScopeSpinBox1.setRange(-1, 99999999)
        self.ui.dataScopeSpinBox2.setRange(-1, 99999999)

        self.ui.yAxisComboBox.addItems(["left", "right", "third"])


    def setupUiGraphFrameDetail(self, graphPropertyItem):
        #self.clearUiPlotDetail()
        self.ui.plotTreeWidget.clear()

        for key in sorted(eval(graphPropertyItem.text(5)).keys()):
            plotSetting = eval(graphPropertyItem.text(5))[key]
            plotPropertyItem = self.getTreeWidgetItemFromPlotSetting(plotSetting)
            
            self.ui.plotTreeWidget.addTopLevelItem(plotPropertyItem)


    def setupUiPlotDetail(self, plotPropertyItem = None):
        if plotPropertyItem:
            self.ui.styleComboBox.currentIndexChanged.disconnect(self.slot1)
            self.ui.plotColorEdit.textChanged.disconnect(self.slot1)
            self.ui.xComboBox.currentIndexChanged.disconnect(self.slot1)
            self.ui.yComboBox.currentIndexChanged.disconnect(self.slot1)
            self.ui.dataScopeSpinBox1.valueChanged.disconnect(self.slot1)
            self.ui.dataScopeSpinBox2.valueChanged.disconnect(self.slot1)
            self.ui.yAxisComboBox.currentIndexChanged.disconnect(self.slot1)

            index = self.ui.styleComboBox.findText(plotPropertyItem.text(7))
            self.ui.styleComboBox.setCurrentIndex(index)
        
            self.ui.plotColorEdit.setText(plotPropertyItem.text(1))
            self.ui.xComboBox.setCurrentIndex(self.getDataIndexFromId(plotPropertyItem.text(4)))
            self.ui.yComboBox.setCurrentIndex(self.getDataIndexFromId(plotPropertyItem.text(5)))
            self.ui.dataScopeSpinBox1.setValue(int(plotPropertyItem.text(2)))
            self.ui.dataScopeSpinBox2.setValue(int(plotPropertyItem.text(3)))
            self.ui.yAxisComboBox.setCurrentIndex(int(plotPropertyItem.text(6)))

            self.ui.styleComboBox.currentIndexChanged.connect(self.slot1)
            self.ui.plotColorEdit.textChanged.connect(self.slot1)
            self.ui.xComboBox.currentIndexChanged.connect(self.slot1)
            self.ui.yComboBox.currentIndexChanged.connect(self.slot1)
            self.ui.dataScopeSpinBox1.valueChanged.connect(self.slot1)
            self.ui.dataScopeSpinBox2.valueChanged.connect(self.slot1)
            self.ui.yAxisComboBox.currentIndexChanged.connect(self.slot1)


    def updatePlotPropertyItem(self, title = "", color = "", dataScopeMax = 0, dataScopeMin = 0, x = "", y = "", yAxis = 0, style = ""):
        if self.ui.plotTreeWidget.currentItem():
            plotPropertyItem = self.ui.plotTreeWidget.currentItem()

            plotPropertyItem.setText(0, title)
            plotPropertyItem.setText(1, color)
            plotPropertyItem.setText(2, str(dataScopeMax))
            plotPropertyItem.setText(3, str(dataScopeMin))
            plotPropertyItem.setText(4, x)
            plotPropertyItem.setText(5, y)
            plotPropertyItem.setText(6, str(yAxis))
            plotPropertyItem.setText(7, style)
            plotPropertyItem.setText(8, self.getDataNameList()[self.getDataIndexFromId(x)])
            plotPropertyItem.setText(9, self.getDataNameList()[self.getDataIndexFromId(y)])
            plotPropertyItem.setText(10, ["Left", "Right", "Third"][yAxis])

            self.plotSettingChanged.emit()

    
    def getTreeWidgetItemFromPlotSetting(self, plotSetting = Setting().getInitSettings()["graphSet"]["graphSet1"]["graphs"]["graph1"]["plots"]["plot1"]):
        item = QTreeWidgetItem([""])
        
        item.setText(0, plotSetting["title"])
        item.setText(1, plotSetting["color"])
        item.setText(2, str(plotSetting["dataScopeMax"]))
        item.setText(3, str(plotSetting["dataScopeMin"]))
        item.setText(4, plotSetting["x"])
        item.setText(5, plotSetting["y"])
        item.setText(6, str(plotSetting["yAxis"]))
        item.setText(7, plotSetting["style"])
        item.setText(8, self.getDataNameList()[self.getDataIndexFromId(plotSetting["x"])])
        item.setText(9, self.getDataNameList()[self.getDataIndexFromId(plotSetting["y"])])
        item.setText(10, ["Left", "Right", "Third"][plotSetting["yAxis"]])

        return item


    def getDataNameList(self):
        dataNameList = list()
        
        dataNameList.append("Data index")
        dataNameList.append("1 (Constant num)")
        
        i = 0
        while i < len(self.tempDataSetSetting["rawData"]):
            dataNameList.append(self.tempDataSetSetting["rawData"]["rawData" + str(i + 1)]["name"])
            i += 1
        i = 0
        while i < len(self.tempDataSetSetting["calcData"]):
            dataNameList.append(self.tempDataSetSetting["calcData"]["calcData" + str(i + 1)]["name"])
            i += 1

        return dataNameList

    
    def getDataNameList2(self):
        dataNameList = list()
        
        dataNameList.append("Default data 1: Data index")
        dataNameList.append("Default data 2: 1 (Constant num)")
        
        i = 0
        while i < len(self.tempDataSetSetting["rawData"]):
            dataNameList.append("Raw data " + str(i + 1) + ": " + self.tempDataSetSetting["rawData"]["rawData" + str(i + 1)]["name"])
            i += 1
        i = 0
        while i < len(self.tempDataSetSetting["calcData"]):
            dataNameList.append("Calc data " + str(i + 1) + ": " + self.tempDataSetSetting["calcData"]["calcData" + str(i + 1)]["name"])
            i += 1

        return dataNameList


    #def clearUiPlotDetail(self):
    #    pass


    def getDataIndexFromId(self, dataID):
        defaultDataNum = 2
        rawDataNum = len(self.tempDataSetSetting["rawData"])
        calcDataNum = len(self.tempDataSetSetting["calcData"])

        if dataID[0] == "d":
            return int(dataID[1:]) - 1
        elif dataID[0] == "r":
            return defaultDataNum + int(dataID[1:]) - 1
        elif dataID[0] == "c":
            return defaultDataNum + rawDataNum + int(dataID[1:]) - 1


    def getDataIdFromIndex(self, dataIndex):
        defaultDataNum = 2
        rawDataNum = len(self.tempDataSetSetting["rawData"])###############
        calcDataNum = len(self.tempDataSetSetting["calcData"])#############

        if dataIndex <= 1:
            return "d" + str(dataIndex + 1)
        elif dataIndex <= rawDataNum + 1:
            return "r" + str(dataIndex - defaultDataNum + 1)
        elif dataIndex <= rawDataNum + calcDataNum + 1:
            return "c" + str(dataIndex - defaultDataNum - rawDataNum + 1)


    def insertTreeWidgetItem(self, treeWidget = None, index = -1, item = None):
        if treeWidget is None:
            return

        if item is None:
            item = self.getTreeWidgetItemFromPlotSetting()

        if index != -1:
            treeWidget.insertTopLevelItem(index + 1, item)
        else:
            treeWidget.addTopLevelItem(item)

        self.plotSettingChanged.emit()
            

    def moveTreeWidgetItem(self, treeWidget = None, index = 0, direction = 0):
        if treeWidget is None:
            return
        if index == 0 and direction == -1:
            return
        if index == treeWidget.topLevelItemCount() - 1 and direction == +1:
            return

        item = treeWidget.takeTopLevelItem(index)
        treeWidget.insertTopLevelItem(index + direction, item)
        treeWidget.setCurrentItem(item)

        self.plotSettingChanged.emit()
        

    def deleteTreeWidgetItem(self, treeWidget = None, index = -1):
        item = treeWidget.takeTopLevelItem(index)
        del item

        self.plotSettingChanged.emit()
        

    def getPlotSettings(self):
        plotSetting = dict()

        i = 0
        while i < self.ui.plotTreeWidget.topLevelItemCount():
            plotSetting["plot" + str(i + 1)] = self.getPlotSettingFromTreeWidgetItem(item = self.ui.plotTreeWidget.topLevelItem(i))

            i += 1

        return plotSetting


    def getPlotSettingFromTreeWidgetItem(self, item = None):
        plotSetting = dict()

        plotSetting = {}
        plotSetting["title"] = item.text(0)
        plotSetting["color"] = item.text(1)
        plotSetting["dataScopeMax"] = int(item.text(2))
        plotSetting["dataScopeMin"] = int(item.text(3))
        plotSetting["x"] = item.text(4)
        plotSetting["y"] = item.text(5)
        plotSetting["yAxis"] = int(item.text(6))
        plotSetting["style"] = item.text(7)

        return plotSetting
