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

class GraphSetSettingWidget(QDialog):
    graphSetSettingsChanged = Signal()

    def __init__(self, parent = None, graphSetSettings = {}, dataSetSettings = {}):
        super(GraphSetSettingWidget, self).__init__(parent)
        
        self.tempGraphSetSettings = graphSetSettings
        self.tempDataSetSettings = dataSetSettings

        self.ui = QUiLoader().load("./graphSetSettingWidget.ui")
        self.setupUi()

        self.ui.graphSetTreeWidget.currentItemChanged.connect(lambda: self.setupUiGraphSetDetail(self.ui.graphSetTreeWidget.currentItem()))

        self.slot1 = lambda: self.updateGraphSetPropertyItem(title = self.ui.graphSetTitleEdit.text(), 
                                                             dataSetIndex = self.ui.dataSetComboBox.currentIndex() + 1)
        self.ui.graphSetTitleEdit.textChanged.connect(self.slot1)
        self.ui.dataSetComboBox.currentIndexChanged.connect(self.slot1)


        self.ui.graphSetNewButton.clicked.connect(lambda: self.insertTreeWidgetItem(treeWidget = self.ui.graphSetTreeWidget, 
                                                                                index = self.ui.graphSetTreeWidget.indexOfTopLevelItem(self.ui.graphSetTreeWidget.currentItem())))
        self.ui.graphSetCopyButton.clicked.connect(lambda: self.insertTreeWidgetItem(treeWidget = self.ui.graphSetTreeWidget, 
                                                                                 index = self.ui.graphSetTreeWidget.indexOfTopLevelItem(self.ui.graphSetTreeWidget.currentItem()), 
                                                                                 item = self.ui.graphSetTreeWidget.currentItem().clone()))
        self.ui.graphSetUpButton.clicked.connect(lambda: self.moveTreeWidgetItem(treeWidget = self.ui.graphSetTreeWidget, 
                                                                                index = self.ui.graphSetTreeWidget.indexOfTopLevelItem(self.ui.graphSetTreeWidget.currentItem()), 
                                                                                direction = -1))
        self.ui.graphSetDownButton.clicked.connect(lambda: self.moveTreeWidgetItem(treeWidget = self.ui.graphSetTreeWidget, 
                                                                                index = self.ui.graphSetTreeWidget.indexOfTopLevelItem(self.ui.graphSetTreeWidget.currentItem()), 
                                                                                direction = +1))
        self.ui.graphSetDeleteButton.clicked.connect(lambda: self.deleteTreeWidgetItem(treeWidget = self.ui.graphSetTreeWidget, 
                                                                                   index = self.ui.graphSetTreeWidget.indexOfTopLevelItem(self.ui.graphSetTreeWidget.currentItem())))

   
    def setupUi(self):
        self.ui.graphSetEnableButton.setEnabled(False)

        self.ui.graphSetTreeWidget.setHeaderLabels(["Title", "id", "enable", "antialias", "dataSet", "graphs", "Data set", "Number of graphs"])
        
        i = 1
        while i < 6:
            self.ui.graphSetTreeWidget.setColumnHidden(i, True)
            i += 1

        header = self.ui.graphSetTreeWidget.header()
        #header.moveSection(0, 0) # "Title" -> 0
        header.moveSection(6, 1) # "Data set" -> 1
        header.moveSection(7, 2) # "Num of graphs" -> 2

        i = 0
        while i < len(self.tempGraphSetSettings.keys()):
            graphSetSetting = self.tempGraphSetSettings["graphSet" + str(i + 1)]
            graphSetPropertyItem = self.getTreeWidgetItemFromGraphSetSetting(graphSetSetting)

            self.ui.graphSetTreeWidget.addTopLevelItem(graphSetPropertyItem)

            i += 1

        dataSetTitleList = self.getDataSetTitleList()
        self.ui.dataSetComboBox.addItems(dataSetTitleList)


    def setupUiGraphSetDetail(self, graphSetPropertyItem = None):
        if graphSetPropertyItem:
            self.ui.graphSetTitleEdit.textChanged.disconnect(self.slot1)
            self.ui.dataSetComboBox.currentIndexChanged.disconnect(self.slot1)

            self.ui.graphSetTitleEdit.setText(graphSetPropertyItem.text(0))

            self.ui.dataSetComboBox.setCurrentIndex(eval(graphSetPropertyItem.text(4))["index"] - 1)
            
            self.ui.graphSetTitleEdit.textChanged.connect(self.slot1)
            self.ui.dataSetComboBox.currentIndexChanged.connect(self.slot1)


    def getDataSetTitleList(self):
        dataSetTitlelist = list()

        for key in sorted(self.tempDataSetSettings.keys()):
            dataSetTitlelist.append(self.tempDataSetSettings[key]["title"])

        return dataSetTitlelist


    def getTreeWidgetItemFromGraphSetSetting(self, graphSetSetting = Setting().getInitSettings()["graphSet"]["graphSet1"]):
        item = QTreeWidgetItem([""])
        item.setText(0, graphSetSetting["title"])    
        item.setText(1, graphSetSetting["id"])
        item.setText(2, str(graphSetSetting["enable"]))
        item.setText(3, str(graphSetSetting["antialias"]))
        item.setText(4, str(graphSetSetting["dataSet"]))
        item.setText(5, str(graphSetSetting["graphs"]))
        
        item.setText(6, str(self.getDataSetTitleList()[graphSetSetting["dataSet"]["index"] - 1]))
        item.setText(7, str(len(graphSetSetting["graphs"].keys())))

        return item


    def updateGraphSetPropertyItem(self, title = "", dataSetIndex = 0):
        if self.ui.graphSetTreeWidget.currentItem():
            graphSetPropertyItem = self.ui.graphSetTreeWidget.currentItem()

            graphSetPropertyItem.setText(0, title)
            #graphSetPropertyItem.setText(1, self.ui.graphSetTreeWidget.currentItem().text(1))
            #graphSetPropertyItem.setText(2, self.ui.graphSetTreeWidget.currentItem().text(2))
            #graphSetPropertyItem.setText(3, self.ui.graphSetTreeWidget.currentItem().text(3))

            dataSet = {
                "index": "dataSet" + str(dataSetIndex), 
                "id": self.tempDataSetSettings["dataSet" + str(dataSetIndex)]["id"]
                }
            graphSetPropertyItem.setText(4, str(dataSet))
            #graphSetPropertyItem.setText(5, self.ui.graphSetTreeWidget.currentItem().text(5))
            
            n = len("dataSet")
            graphSetPropertyItem.setText(6, str(self.getDataSetTitleList()[int(dataSetIndex) - 1]))

            #graphSetPropertyItem.setText(7, self.ui.graphSetTreeWidget.currentItem().text(7))


    def getCurrentGraphSetSettings(self):
        graphSetSettings = dict()

        i = 0
        while i < self.ui.graphSetTreeWidget.topLevelItemCount():
            graphSetSettings["graphSet" + str(i + 1)] = self.getGraphSetSettingFromTreeWidgetItem(item = self.ui.graphSetTreeWidget.topLevelItem(i))

            i += 1

        return graphSetSettings


    def getGraphSetSettingFromTreeWidgetItem(self, item = None):
        graphSetSetting = dict()

        graphSetSetting["title"] = item.text(0)
        graphSetSetting["id"] = item.text(1)
        
        import ast
        graphSetSetting["enable"] = ast.literal_eval(item.text(2))
        graphSetSetting["antialias"] = ast.literal_eval(item.text(3))
        graphSetSetting["dataSet"] = eval(item.text(4))
        graphSetSetting["graphs"] = eval(item.text(5))

        return graphSetSetting

    
    def insertTreeWidgetItem(self, treeWidget = None, index = -1, item = None):
        if treeWidget is None:
            return

        if item is None:
            item = self.getTreeWidgetItemFromGraphSetSetting()

        if index != -1:
            treeWidget.insertTopLevelItem(index + 1, item)
        else:
            treeWidget.addTopLevelItem(item)

        self.graphSetSettingsChanged.emit()


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

        self.graphSetSettingsChanged.emit()


    def deleteTreeWidgetItem(self, treeWidget = None, index = -1):
        item = treeWidget.takeTopLevelItem(index)
        del item

        self.graphSetSettingsChanged.emit()
