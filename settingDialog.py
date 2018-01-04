#-------------------------------------------------------------------------------
# Name:        GraphSIDE
# Author:      nebula121 <nebula121.dev@gmail.com>
# Copyright:   (c) nebula121 2018
# Licence:     MIT License
#-------------------------------------------------------------------------------

import sys
import copy
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtUiTools import QUiLoader
from graphSetSetting import GraphSetSettingWidget
from graphSetting import GraphSettingWidget
from dataSetSettingWidget import DataSetSettingWidget
from dataSetting import DataSettingWidget
from generalSetting import GeneralSettingWidget

class SettingDialog(QDialog):
    
    def __init__(self, parent = None, settings = {}):
        super(SettingDialog, self).__init__(parent)
        
        self.tempSettings = copy.deepcopy(settings)

        self.ui = QUiLoader().load("./settingDialog.ui")
        self.setupUi()
        
        #self.slot1 = self.openSettingWidget(item = current, previousItem = previous)
        #self.ui.treeWidget.currentItemChanged.connect(lambda: self.openSettingWidget(self.ui.treeWidget.currentItem()))
        self.ui.treeWidget.currentItemChanged.connect(self.openSettingWidget)
        self.ui.buttonBox.accepted.connect(lambda: self.ui.accept())
        self.ui.buttonBox.rejected.connect(lambda: self.ui.reject())


    def setupUi(self):
        self.treeWidgetTopItems = [QTreeWidgetItem(["General"]), 
                                   QTreeWidgetItem(["Data Set"]), 
                                   QTreeWidgetItem(["Graph Set"])]

        self.ui.treeWidget.addTopLevelItems(self.treeWidgetTopItems)

        self.treeWidgetDataSetItems = list()
        self.treeWidgetDataSetItems.append(QTreeWidgetItem(["全般"]))

        i = 1
        while i <= len(self.tempSettings["dataSet"]):
            key = "dataSet" + str(i)
            item = QTreeWidgetItem()
            item.setText(0, self.tempSettings["dataSet"][key]["title"])
            item.setText(1, key)
            self.treeWidgetDataSetItems.append(item)

            i += 1
            
        self.treeWidgetGraphSetItems = list()
        self.treeWidgetGraphSetItems.append(QTreeWidgetItem(["全般"]))

        i = 1
        while i <= len(self.tempSettings["graphSet"]):
            key = "graphSet" + str(i)
            item = QTreeWidgetItem()
            item.setText(0, self.tempSettings["graphSet"][key]["title"])
            item.setText(1, key)
            self.treeWidgetGraphSetItems.append(item)

            i += 1
            
        self.treeWidgetTopItems[1].addChildren(self.treeWidgetDataSetItems)
        self.treeWidgetTopItems[2].addChildren(self.treeWidgetGraphSetItems)
        
        self.openSettingWidget(self.ui.treeWidget.topLevelItem(0), None)

        self.ui.setWindowTitle("設定")


    def openSettingWidget(self, item, previousItem):
        if previousItem:
            self.updateTempSetting(previousItem)

        if self.ui.treeWidget.indexOfTopLevelItem(item) == 0:
            self.widget = GeneralSettingWidget(generalSetting = self.tempSettings["general"], shortcutSetting = self.tempSettings["shortcut"])
            self.ui.verticalLayout.itemAt(0).widget().deleteLater()
            self.ui.verticalLayout.insertWidget(0, self.widget.ui)
            return
        elif self.ui.treeWidget.indexOfTopLevelItem(item) == 1:
            self.widget = DataSetSettingWidget(dataSetSettings = self.tempSettings["dataSet"])
            self.widget.dataSetSettingsChanged.connect(lambda: self.updataTreeWidgetItemsDataSet())
            self.ui.verticalLayout.itemAt(0).widget().deleteLater()
            self.ui.verticalLayout.insertWidget(0, self.widget.ui)
            return
        elif self.ui.treeWidget.indexOfTopLevelItem(item) == 2:
            self.widget = GraphSetSettingWidget(graphSetSettings = self.tempSettings["graphSet"], 
                                                dataSetSettings = self.tempSettings["dataSet"])
            self.widget.graphSetSettingsChanged.connect(lambda: self.updataTreeWidgetItemsGraphSet())
            self.ui.verticalLayout.itemAt(0).widget().deleteLater()
            self.ui.verticalLayout.insertWidget(0, self.widget.ui)
            return
        elif self.ui.treeWidget.indexOfTopLevelItem(item) == -1:
            if self.ui.treeWidget.indexOfTopLevelItem(item.parent()) == 1:
                if item.parent().indexOfChild(item) == 0:
                    self.widget = DataSetSettingWidget(dataSetSettings = self.tempSettings["dataSet"])
                    self.widget.dataSetSettingsChanged.connect(lambda: self.updataTreeWidgetItemsDataSet())
                else:
                    self.widget = DataSettingWidget(dataSetSetting = self.tempSettings["dataSet"][item.text(1)])
                self.ui.verticalLayout.itemAt(0).widget().deleteLater()
                self.ui.verticalLayout.insertWidget(0, self.widget.ui)
                return
            elif self.ui.treeWidget.indexOfTopLevelItem(item.parent()) == 2:
                if item.parent().indexOfChild(item) == 0:
                    self.widget = GraphSetSettingWidget(graphSetSettings = self.tempSettings["graphSet"], 
                                                   dataSetSettings = self.tempSettings["dataSet"])
                    self.widget.graphSetSettingsChanged.connect(lambda: self.updataTreeWidgetItemsGraphSet())
                else:
                    self.widget = GraphSettingWidget(generalSetting = self.tempSettings["general"], 
                                                     graphSetSetting = self.tempSettings["graphSet"][item.text(1)], 
                                                     dataSetSetting = self.tempSettings["dataSet"]["dataSet" + str(self.tempSettings["graphSet"][item.text(1)]["dataSet"]["index"])])
                self.ui.verticalLayout.itemAt(0).widget().deleteLater()
                self.ui.verticalLayout.insertWidget(0, self.widget.ui)
                return
            else:
                self.widget = QLabel("Eroor")
        else:
            self.widget = QLabel("Eroor")

        self.ui.verticalLayout.itemAt(0).widget().deleteLater()
        self.ui.verticalLayout.insertWidget(0, self.widget)


    def updateTempSetting(self, item):
        if self.ui.treeWidget.indexOfTopLevelItem(item) == 0:
            self.tempSettings["general"] = self.widget.getCurrentGeneralSetting()
            self.tempSettings["shortcut"] = self.widget.getCurrentShortcutSettings()
            return
        elif self.ui.treeWidget.indexOfTopLevelItem(item) == 1:
            self.tempSettings["dataSet"] = self.widget.getCurrentDataSetSettings()
            return
        elif self.ui.treeWidget.indexOfTopLevelItem(item) == 2:
            self.tempSettings["graphSet"] = self.widget.getCurrentGraphSetSettings()
            return
        elif self.ui.treeWidget.indexOfTopLevelItem(item) == -1:
            if self.ui.treeWidget.indexOfTopLevelItem(item.parent()) == 1:
                if item.parent().indexOfChild(item) == 0:
                    self.tempSettings["dataSet"] = self.widget.getCurrentDataSetSettings()
                else:
                    self.tempSettings["dataSet"]["dataSet" + str(item.parent().indexOfChild(item))] = self.widget.getCurrentDataSetting()
                return
            elif self.ui.treeWidget.indexOfTopLevelItem(item.parent()) == 2:
                if item.parent().indexOfChild(item) == 0:
                    self.tempSettings["graphSet"] = self.widget.getCurrentGraphSetSettings()
                else:
                    self.tempSettings["graphSet"]["graphSet" + str(item.parent().indexOfChild(item))]["graphs"] = self.widget.getCurrentGraphSettings()
                return


    def updataTreeWidgetItemsDataSet(self):
        self.tempSettings["dataSet"] = self.widget.getCurrentDataSetSettings()

        while self.ui.treeWidget.topLevelItem(1).childCount() > 1:
            self.ui.treeWidget.topLevelItem(1).takeChild(1)
        
        self.treeWidgetDataSetItems = list()

        i = 1
        while i <= len(self.tempSettings["dataSet"]):
            key = "dataSet" + str(i)
            item = QTreeWidgetItem()
            item.setText(0, self.tempSettings["dataSet"][key]["title"])
            item.setText(1, key)
            self.treeWidgetDataSetItems.append(item)

            i += 1
            
        self.ui.treeWidget.topLevelItem(1).addChildren(self.treeWidgetDataSetItems)

        self.ui.treeWidget.expandItem(self.ui.treeWidget.topLevelItem(1))
    
    
    def updataTreeWidgetItemsGraphSet(self):
        self.tempSettings["graphSet"] = self.widget.getCurrentGraphSetSettings()
        
        while self.ui.treeWidget.topLevelItem(2).childCount() > 1:
            self.ui.treeWidget.topLevelItem(2).takeChild(1)
        
        self.treeWidgetGraphSetItems = list()

        i = 1
        while i <= len(self.tempSettings["graphSet"]):
            key = "graphSet" + str(i)
            item = QTreeWidgetItem()
            item.setText(0, self.tempSettings["graphSet"][key]["title"])
            item.setText(1, key)
            self.treeWidgetGraphSetItems.append(item)

            i += 1
            
        self.ui.treeWidget.topLevelItem(2).addChildren(self.treeWidgetGraphSetItems)

        self.ui.treeWidget.expandItem(self.ui.treeWidget.topLevelItem(2))



if __name__ == '__main__':
    # Qt Applicationを作ります
    app = QApplication(sys.argv)

    import os
    from setting import Setting    
    if os.path.exists(".\\settings.json"):
        settingsClass = Setting(filePath = ".\\settings.json")
    else:
        settingsClass = Setting()
    settings = settingsClass.settings

    # formを作成して表示します
    mainWin = SettingDialog(settings = settings)
    mainWin.ui.show()
    # Qtのメインループを開始します
    sys.exit(app.exec_())