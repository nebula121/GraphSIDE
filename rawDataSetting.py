#-------------------------------------------------------------------------------
# Name:        GraphSIDE
# Author:      nebula121 <nebula121.dev@gmail.com>
# Copyright:   (c) nebula121 2018
# Licence:     MIT License
#-------------------------------------------------------------------------------

import sys
from PySide.QtCore import *
from PySide.QtGui import *
from setting import Setting

class RawDataSettingWidget(QDialog):
    
    def __init__(self, parent = None, dataSettingWidgetUi = None, dataSetSetting = {}):
        super(RawDataSettingWidget, self).__init__(parent)
        
        self.tempDataSetSetting = dataSetSetting
        self.ui = dataSettingWidgetUi

        self.ui.rawDataTreeWidget.currentItemChanged.connect(lambda: self.setupUiRawDataDetail(self.ui.rawDataTreeWidget.currentItem()))

        self.slot1 = lambda: self.setRawDataSetting(name = self.ui.rawDataNameEdit.text(), coefficient = self.ui.rawDataCoefficientSpinBox.value())
        self.ui.rawDataNameEdit.textChanged.connect(self.slot1)
        self.ui.rawDataCoefficientSpinBox.valueChanged.connect(self.slot1)
        
        self.ui.rawDataNewButton.clicked.connect(lambda: self.insertRawDataSetting(index = self.ui.rawDataTreeWidget.indexOfTopLevelItem(self.ui.rawDataTreeWidget.currentItem())))
        self.ui.rawDataCopyButton.clicked.connect(lambda: self.insertRawDataSetting(index = self.ui.rawDataTreeWidget.indexOfTopLevelItem(self.ui.rawDataTreeWidget.currentItem()), 
                                                                                    rawDataProperty = self.ui.rawDataTreeWidget.currentItem().clone()))
        self.ui.rawDataUpButton.clicked.connect(lambda: self.moveTreeWidgetItem(treeWidget = self.ui.rawDataTreeWidget, 
                                                                                index = self.ui.rawDataTreeWidget.indexOfTopLevelItem(self.ui.rawDataTreeWidget.currentItem()), 
                                                                                direction = -1))
        self.ui.rawDataDownButton.clicked.connect(lambda: self.moveTreeWidgetItem(treeWidget = self.ui.rawDataTreeWidget, 
                                                                                index = self.ui.rawDataTreeWidget.indexOfTopLevelItem(self.ui.rawDataTreeWidget.currentItem()), 
                                                                                direction = +1))
        self.ui.rawDataDeleteButton.clicked.connect(lambda: self.deleteShortcutSetting(treeWidget = self.ui.rawDataTreeWidget, 
                                                                                       index = self.ui.rawDataTreeWidget.indexOfTopLevelItem(self.ui.rawDataTreeWidget.currentItem())))

        
    def setupUi(self):
        self.ui.rawDataTreeWidget.setHeaderLabels(["Column", "Name", "Coefficient"])

        i = 0
        while i < len(self.tempDataSetSetting["rawData"]):
            rawDataProperty = self.getRawDataPropertyFromSetting(self.tempDataSetSetting["rawData"]["rawData" + str(i + 1)])

            self.ui.rawDataTreeWidget.addTopLevelItem(rawDataProperty)

            i += 1

        self.updateRawDataTreeWidgetIndexNum()
        self.ui.rawDataCoefficientSpinBox.setDecimals(6)
        self.ui.rawDataCoefficientSpinBox.setRange(-999999999999., 999999999999.)


    def setupUiRawDataDetail(self, rawDataProperty):
        if rawDataProperty:
            self.ui.rawDataNameEdit.textChanged.disconnect(self.slot1)
            self.ui.rawDataCoefficientSpinBox.valueChanged.disconnect(self.slot1)
        
            self.ui.rawDataNameEdit.setText(rawDataProperty.text(1))
            self.ui.rawDataCoefficientSpinBox.setValue(float(rawDataProperty.text(2)))

            self.ui.rawDataNameEdit.textChanged.connect(self.slot1)
            self.ui.rawDataCoefficientSpinBox.valueChanged.connect(self.slot1)


    def getRawDataPropertyFromSetting(self, rawDataSetting = Setting().getInitSettings()["dataSet"]["dataSet1"]["rawData"]["rawData1"]):
        rawDataProperty = QTreeWidgetItem([""])

        rawDataProperty.setText(1, rawDataSetting["name"])
        rawDataProperty.setText(2, str(rawDataSetting["coefficient"]))

        return rawDataProperty


    def setRawDataSetting(self, name = "", coefficient = 1.0):
        if self.ui.rawDataTreeWidget.currentItem():
            rawDataProperty = self.ui.rawDataTreeWidget.currentItem()

            rawDataProperty.setText(1, name)
            rawDataProperty.setText(2, str(coefficient))


    def insertRawDataSetting(self, index = -1, rawDataProperty = None):
        if rawDataProperty is None:
            rawDataProperty = self.getRawDataPropertyFromSetting()

        if index != -1:
            self.ui.rawDataTreeWidget.insertTopLevelItem(index + 1, rawDataProperty)
        else:
            self.ui.rawDataTreeWidget.addTopLevelItem(rawDataProperty)

        self.updateRawDataTreeWidgetIndexNum()


    def updateRawDataTreeWidgetIndexNum(self):
        i = 0

        while i < self.ui.rawDataTreeWidget.topLevelItemCount():
            self.ui.rawDataTreeWidget.topLevelItem(i).setText(0, str(i + 1))

            i += 1


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

        if treeWidget is self.ui.rawDataTreeWidget:
            self.updateRawDataTreeWidgetIndexNum()


    def deleteShortcutSetting(self, treeWidget = None, index = -1):
        item = treeWidget.takeTopLevelItem(index)
        del item


    def getCurrentRawDataSetting(self):
        rawDataSetting = dict()

        i = 0
        while i < self.ui.rawDataTreeWidget.topLevelItemCount():
            rawDataSetting["rawData" + str(i + 1)] = {}
            rawDataSetting["rawData" + str(i + 1)]["name"] = self.ui.rawDataTreeWidget.topLevelItem(i).text(1)
            rawDataSetting["rawData" + str(i + 1)]["coefficient"] = float(self.ui.rawDataTreeWidget.topLevelItem(i).text(2))

            i += 1

        return rawDataSetting