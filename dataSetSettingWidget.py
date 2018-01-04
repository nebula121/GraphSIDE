#-------------------------------------------------------------------------------
# Name:        GraphSIDE
# Author:      nebula121 <nebula121.dev@gmail.com>
# Copyright:   (c) nebula121 2018
# Licence:     MIT License
#-------------------------------------------------------------------------------

import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtUiTools import QUiLoader
from setting import Setting

class DataSetSettingWidget(QDialog):
    dataSetSettingsChanged = Signal()

    def __init__(self, parent = None, dataSetSettings = {}):
        super(DataSetSettingWidget, self).__init__(parent)
        
        self.tempDataSetSettings = dataSetSettings

        self.ui = QUiLoader().load("./dataSetSettingWidget.ui")
        self.setupUi()

        self.ui.dataSetTreeWidget.currentItemChanged.connect(lambda: self.setupUiDataSetDetail(self.ui.dataSetTreeWidget.currentItem()))

        self.slot1 = lambda: self.updateDataSetPropertyItem(title = self.ui.dataSetTitleEdit.text())
        self.ui.dataSetTitleEdit.textChanged.connect(self.slot1)

        self.ui.dataSetNewButton.clicked.connect(lambda: self.insertTreeWidgetItem(treeWidget = self.ui.dataSetTreeWidget, 
                                                                                index = self.ui.dataSetTreeWidget.indexOfTopLevelItem(self.ui.dataSetTreeWidget.currentItem())))
        self.ui.dataSetCopyButton.clicked.connect(lambda: self.insertTreeWidgetItem(treeWidget = self.ui.dataSetTreeWidget, 
                                                                                 index = self.ui.dataSetTreeWidget.indexOfTopLevelItem(self.ui.dataSetTreeWidget.currentItem()), 
                                                                                 item = self.ui.dataSetTreeWidget.currentItem().clone()))
        self.ui.dataSetUpButton.clicked.connect(lambda: self.moveTreeWidgetItem(treeWidget = self.ui.dataSetTreeWidget, 
                                                                                index = self.ui.dataSetTreeWidget.indexOfTopLevelItem(self.ui.dataSetTreeWidget.currentItem()), 
                                                                                direction = -1))
        self.ui.dataSetDownButton.clicked.connect(lambda: self.moveTreeWidgetItem(treeWidget = self.ui.dataSetTreeWidget, 
                                                                                index = self.ui.dataSetTreeWidget.indexOfTopLevelItem(self.ui.dataSetTreeWidget.currentItem()), 
                                                                                direction = +1))
        self.ui.dataSetDeleteButton.clicked.connect(lambda: self.deleteTreeWidgetItem(treeWidget = self.ui.dataSetTreeWidget, 
                                                                                   index = self.ui.dataSetTreeWidget.indexOfTopLevelItem(self.ui.dataSetTreeWidget.currentItem())))

   
    def setupUi(self):
        self.ui.dataSetEnableButton.setEnabled(False)

        self.ui.dataSetTreeWidget.setHeaderLabels(["Title", "id", "enable", "headerNum", "rawData", "calcData", "Num of raw data", "Num of calc data"])
        
        i = 1
        while i < 6:
            self.ui.dataSetTreeWidget.setColumnHidden(i, True)
            i += 1

        header = self.ui.dataSetTreeWidget.header()
        #header.moveSection(0, 0) # "Title" -> 0
        header.moveSection(6, 1) # "Num of raw data" -> 1
        header.moveSection(7, 2) # "Num of calc data" -> 2

        i = 0
        while i < len(self.tempDataSetSettings.keys()):
            dataSetSetting = self.tempDataSetSettings["dataSet" + str(i + 1)]
            dataSetPropertyItem = self.getTreeWidgetItemFromDataSetSetting(dataSetSetting)

            self.ui.dataSetTreeWidget.addTopLevelItem(dataSetPropertyItem)

            i += 1
         

    def setupUiDataSetDetail(self, dataSetPropertyItem = None):
        if dataSetPropertyItem:
            self.ui.dataSetTitleEdit.textChanged.disconnect(self.slot1)

            self.ui.dataSetTitleEdit.setText(dataSetPropertyItem.text(0))
            
            self.ui.dataSetTitleEdit.textChanged.connect(self.slot1)


    def getTreeWidgetItemFromDataSetSetting(self, dataSetSetting = Setting().getInitSettings()["dataSet"]["dataSet1"]):
        item = QTreeWidgetItem([""])
        item.setText(0, dataSetSetting["title"])    
        item.setText(1, dataSetSetting["id"])
        item.setText(2, str(dataSetSetting["enable"]))
        item.setText(3, str(dataSetSetting["headerNum"]))
        item.setText(4, str(dataSetSetting["rawData"]))
        item.setText(5, str(dataSetSetting["calcData"]))

        item.setText(6, str(len(dataSetSetting["rawData"].keys())))
        item.setText(7, str(len(dataSetSetting["calcData"].keys())))

        return item


    def updateDataSetPropertyItem(self, title = ""):
        if self.ui.dataSetTreeWidget.currentItem():
            dataSetPropertyItem = self.ui.dataSetTreeWidget.currentItem()

            dataSetPropertyItem.setText(0, title)
            #dataSetPropertyItem.setText(1, self.ui.dataSetTreeWidget.currentItem().text(1))
            #dataSetPropertyItem.setText(2, self.ui.dataSetTreeWidget.currentItem().text(2))
            #dataSetPropertyItem.setText(3, self.ui.dataSetTreeWidget.currentItem().text(3))
            #dataSetPropertyItem.setText(4, self.ui.dataSetTreeWidget.currentItem().text(4))
            #dataSetPropertyItem.setText(5, self.ui.dataSetTreeWidget.currentItem().text(5))
            
            #dataSetPropertyItem.setText(6, self.ui.dataSetTreeWidget.currentItem().text(6))
            #dataSetPropertyItem.setText(7, self.ui.dataSetTreeWidget.currentItem().text(7))


    def getCurrentDataSetSettings(self):
        dataSetSettings = dict()

        i = 0
        while i < self.ui.dataSetTreeWidget.topLevelItemCount():
            dataSetSettings["dataSet" + str(i + 1)] = self.getDataSettingFromTreeWidgetItem(item = self.ui.dataSetTreeWidget.topLevelItem(i))

            i += 1

        return dataSetSettings


    def getDataSettingFromTreeWidgetItem(self, item = None):
        dataSetSetting = dict()

        dataSetSetting["title"] = item.text(0)
        dataSetSetting["id"] = item.text(1)
        
        import ast
        dataSetSetting["enable"] = ast.literal_eval(item.text(2))
        dataSetSetting["headerNum"] = ast.literal_eval(item.text(3))
        dataSetSetting["rawData"] = eval(item.text(4))
        dataSetSetting["calcData"] = eval(item.text(5))

        return dataSetSetting

    
    def insertTreeWidgetItem(self, treeWidget = None, index = -1, item = None):
        if treeWidget is None:
            return

        if item is None:
            item = self.getTreeWidgetItemFromDataSetSetting()

        if index != -1:
            treeWidget.insertTopLevelItem(index + 1, item)
        else:
            treeWidget.addTopLevelItem(item)

        self.dataSetSettingsChanged.emit()


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
        
        self.dataSetSettingsChanged.emit()


    def deleteTreeWidgetItem(self, treeWidget = None, index = -1):
        item = treeWidget.takeTopLevelItem(index)
        del item

        self.dataSetSettingsChanged.emit()
