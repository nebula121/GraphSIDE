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

class CalcDataSettingWidget(QDialog):
    
    def __init__(self, parent = None, dataSettingWidgetUi = None, dataSetSetting = {}):
        super(CalcDataSettingWidget, self).__init__(parent)
        
        self.tempDataSetSetting = dataSetSetting
        self.ui = dataSettingWidgetUi

        self.ui.calcDataTreeWidget.currentItemChanged.connect(lambda: self.setupUiCalcDataDetail(self.ui.calcDataTreeWidget.currentItem()))

        self.slot2 = lambda: self.setCalcDataSetting(name = self.ui.calcDataNameEdit.text(), 
                                                     firstCoefficient = self.ui.calcFirstDataCoefficientSpinBox.value(), 
                                                     firstDataIndex = self.ui.calcFirstDataComboBox.currentIndex(), 
                                                     operator = self.ui.operatorComboBox.currentText(), 
                                                     secondCoefficient = self.ui.calcSecondDataCoefficientSpinBox.value(), 
                                                     secondDataIndex = self.ui.calcSecondDataComboBox.currentIndex())
        self.ui.calcDataNameEdit.textChanged.connect(self.slot2)
        self.ui.calcFirstDataCoefficientSpinBox.valueChanged.connect(self.slot2)
        self.ui.calcFirstDataComboBox.currentIndexChanged.connect(self.slot2)
        self.ui.operatorComboBox.currentIndexChanged.connect(self.slot2)
        self.ui.calcSecondDataCoefficientSpinBox.valueChanged.connect(self.slot2)
        self.ui.calcSecondDataComboBox.currentIndexChanged.connect(self.slot2)
        
        self.ui.calcDataNewButton.clicked.connect(lambda: self.insertCalcDataSetting(index = self.ui.calcDataTreeWidget.indexOfTopLevelItem(self.ui.calcDataTreeWidget.currentItem())))
        self.ui.calcDataCopyButton.clicked.connect(lambda: self.insertCalcDataSetting(index = self.ui.calcDataTreeWidget.indexOfTopLevelItem(self.ui.calcDataTreeWidget.currentItem()), 
                                                                                      calcDataProperty = self.ui.calcDataTreeWidget.currentItem().clone()))
        self.ui.calcDataUpButton.clicked.connect(lambda: self.moveTreeWidgetItem(treeWidget = self.ui.calcDataTreeWidget, 
                                                                                 index = self.ui.calcDataTreeWidget.indexOfTopLevelItem(self.ui.calcDataTreeWidget.currentItem()), 
                                                                                 direction = -1))
        self.ui.calcDataDownButton.clicked.connect(lambda: self.moveTreeWidgetItem(treeWidget = self.ui.calcDataTreeWidget, 
                                                                                   index = self.ui.calcDataTreeWidget.indexOfTopLevelItem(self.ui.calcDataTreeWidget.currentItem()), 
                                                                                   direction = +1))
        self.ui.calcDataDeleteButton.clicked.connect(lambda: self.deleteShortcutSetting(treeWidget = self.ui.calcDataTreeWidget, 
                                                                                       index = self.ui.calcDataTreeWidget.indexOfTopLevelItem(self.ui.calcDataTreeWidget.currentItem())))


    def setupUi(self):
        self.ui.calcDataTreeWidget.setHeaderLabels(["Name", "First Coefficient", "First Data (ID)", "Operator", "First Coefficient", "Second Data (ID)", "First Data", "Second Data"])
        self.ui.calcDataTreeWidget.setColumnHidden(1, True)
        self.ui.calcDataTreeWidget.setColumnHidden(2, True)
        self.ui.calcDataTreeWidget.setColumnHidden(4, True)
        self.ui.calcDataTreeWidget.setColumnHidden(5, True)
        header = self.ui.calcDataTreeWidget.header()
        #header.moveSection(0, 0) # "Name" -> 0
        header.moveSection(6, 1) # "First Data" -> 1
        header.moveSection(4, 2) # "Operator" -> 2
        header.moveSection(7, 3) # "Second Data" -> 3
            
        i = 0
        while i < len(self.tempDataSetSetting["calcData"]):
            calcDataProperty = self.getCalcDataPropertyFromSetting(self.tempDataSetSetting["calcData"]["calcData" + str(i + 1)])

            self.ui.calcDataTreeWidget.addTopLevelItem(calcDataProperty)

            i += 1
        
        self.updateCalcDataComboBox()
        self.ui.operatorComboBox.addItems(["+", "-", ""])
        
        self.ui.calcFirstDataCoefficientSpinBox.setDecimals(6)
        self.ui.calcSecondDataCoefficientSpinBox.setDecimals(6)
        self.ui.calcFirstDataCoefficientSpinBox.setRange(-999999999999., 999999999999.)
        self.ui.calcSecondDataCoefficientSpinBox.setRange(-999999999999., 999999999999.)

            
    def setupUiCalcDataDetail(self, calcDataProperty):
        if calcDataProperty:
            self.ui.calcDataNameEdit.textChanged.disconnect(self.slot2)
            self.ui.calcFirstDataCoefficientSpinBox.valueChanged.disconnect(self.slot2)
            self.ui.calcFirstDataComboBox.currentIndexChanged.disconnect(self.slot2)
            self.ui.operatorComboBox.currentIndexChanged.disconnect(self.slot2)
            self.ui.calcSecondDataCoefficientSpinBox.valueChanged.disconnect(self.slot2)
            self.ui.calcSecondDataComboBox.currentIndexChanged.disconnect(self.slot2)

            self.ui.calcDataNameEdit.setText(calcDataProperty.text(0))
            self.ui.calcFirstDataCoefficientSpinBox.setValue(float(calcDataProperty.text(1)))
            self.ui.calcFirstDataComboBox.setCurrentIndex(self.getDataIndex(calcDataProperty.text(2)))
            self.ui.calcSecondDataCoefficientSpinBox.setValue(float(calcDataProperty.text(4)))
            self.ui.calcSecondDataComboBox.setCurrentIndex(self.getDataIndex(calcDataProperty.text(5)))
        
            index = self.ui.operatorComboBox.findText(calcDataProperty.text(3))
            self.ui.operatorComboBox.setCurrentIndex(index)
           
            self.ui.calcDataNameEdit.textChanged.connect(self.slot2)
            self.ui.calcFirstDataCoefficientSpinBox.valueChanged.connect(self.slot2)
            self.ui.calcFirstDataComboBox.currentIndexChanged.connect(self.slot2)
            self.ui.operatorComboBox.currentIndexChanged.connect(self.slot2)
            self.ui.calcSecondDataCoefficientSpinBox.valueChanged.connect(self.slot2)
            self.ui.calcSecondDataComboBox.currentIndexChanged.connect(self.slot2)
        

    def setCalcDataSetting(self, name = "", firstCoefficient = 1.0, firstDataIndex = 0, operator = "", secondCoefficient = 1.0, secondDataIndex = 0):
        if self.ui.calcDataTreeWidget.currentItem():
            calcDataProperty = self.ui.calcDataTreeWidget.currentItem()

            calcDataProperty.setText(0, name)
            calcDataProperty.setText(1, str(firstCoefficient))
            calcDataProperty.setText(2, self.getDataID(firstDataIndex))
            calcDataProperty.setText(3, operator)
            calcDataProperty.setText(4, str(secondCoefficient))
            calcDataProperty.setText(5, self.getDataID(secondDataIndex))
            calcDataProperty.setText(6, self.getDataNameList()[firstDataIndex])
            calcDataProperty.setText(7, self.getDataNameList()[secondDataIndex])

    
    def getCalcDataPropertyFromSetting(self, calcDataSetting = Setting().getInitSettings()["dataSet"]["dataSet1"]["calcData"]["calcData1"]):
        calcDataProperty = QTreeWidgetItem([""])
        calcDataProperty.setText(0, calcDataSetting["name"])
        calcDataProperty.setText(1, str(calcDataSetting["firstCoefficient"]))
        calcDataProperty.setText(2, calcDataSetting["firstData"])
        calcDataProperty.setText(3, calcDataSetting["operator"])
        calcDataProperty.setText(4, str(calcDataSetting["secondCoefficient"]))
        calcDataProperty.setText(5, calcDataSetting["secondData"])
        calcDataProperty.setText(6, self.getDataNameList()[self.getDataIndex(calcDataSetting["firstData"])])
        calcDataProperty.setText(7, self.getDataNameList()[self.getDataIndex(calcDataSetting["secondData"])])

        return calcDataProperty


    def getDataNameList(self):#############
        dataNameList = list()
        
        dataNameList.append("Default data 1: Data index")
        dataNameList.append("Default data 2: 1 (Constant num)")
        
        i = 0
        while i < self.ui.rawDataTreeWidget.topLevelItemCount():
            dataNameList.append("Raw data " + str(i + 1) + ": " + self.ui.rawDataTreeWidget.topLevelItem(i).text(1))
            i += 1

        return dataNameList


    def getDataIndex(self, dataID):
        defaultDataNum = 2
        rawDataNum = len(self.tempDataSetSetting["rawData"])##############
        calcDataNum = len(self.tempDataSetSetting["calcData"])############

        if dataID[0] == "d":
            return int(dataID[1:]) - 1
        elif dataID[0] == "r":
            return defaultDataNum + int(dataID[1:]) - 1
        elif dataID[0] == "c":
            return defaultDataNum + rawDataNum + int(dataID[1:]) - 1


    def getDataID(self, dataIndex):
        defaultDataNum = 2
        rawDataNum = len(self.tempDataSetSetting["rawData"])###############
        calcDataNum = len(self.tempDataSetSetting["calcData"])#############

        if dataIndex <= 1:
            return "d" + str(dataIndex + 1)
        elif dataIndex <= rawDataNum + 1:
            return "r" + str(dataIndex - defaultDataNum + 1)
        elif dataIndex <= rawDataNum + calcDataNum + 1:
            return "c" + str(dataIndex - defaultDataNum - rawDataNum + 1)


    def updateCalcDataComboBox(self):
        dataNameList = self.getDataNameList()

        if self.ui.calcFirstDataComboBox.currentIndex() != -1:
            calcFirstDataComboBoxIndex = self.ui.calcFirstDataComboBox.currentIndex()
        else:
            calcFirstDataComboBoxIndex = 0
        if self.ui.calcSecondDataComboBox.currentIndex() != -1:
            calcSecondDataComboBoxIndex = self.ui.calcSecondDataComboBox.currentIndex()
        else:
            calcSecondDataComboBoxIndex = 0

        self.ui.calcFirstDataComboBox.clear()
        self.ui.calcSecondDataComboBox.clear()
        
        i = 0
        while i < len(dataNameList):
            self.ui.calcFirstDataComboBox.addItem(dataNameList[i])
            self.ui.calcSecondDataComboBox.addItem(dataNameList[i])
            i += 1

        self.ui.calcFirstDataComboBox.setCurrentIndex(calcFirstDataComboBoxIndex)
        self.ui.calcSecondDataComboBox.setCurrentIndex(calcSecondDataComboBoxIndex)


    def insertCalcDataSetting(self, index = -1, calcDataProperty = None):
        if calcDataProperty is None:
            calcDataProperty = self.getCalcDataPropertyFromSetting()

        if index != -1:
            self.ui.calcDataTreeWidget.insertTopLevelItem(index + 1, calcDataProperty)
        else:
            self.ui.calcDataTreeWidget.addTopLevelItem(calcDataProperty)


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

        
    def getCurrentCalcDataSetting(self):
        calcDataSetting = dict()

        i = 0
        while i < self.ui.calcDataTreeWidget.topLevelItemCount():
            calcDataSetting["calcData" + str(i + 1)] = {}
            calcDataSetting["calcData" + str(i + 1)]["name"] = self.ui.calcDataTreeWidget.topLevelItem(i).text(0)
            calcDataSetting["calcData" + str(i + 1)]["firstCoefficient"] = float(self.ui.calcDataTreeWidget.topLevelItem(i).text(1))
            calcDataSetting["calcData" + str(i + 1)]["firstData"] = self.ui.calcDataTreeWidget.topLevelItem(i).text(2)
            calcDataSetting["calcData" + str(i + 1)]["operator"] = self.ui.calcDataTreeWidget.topLevelItem(i).text(3)
            calcDataSetting["calcData" + str(i + 1)]["secondCoefficient"] = float(self.ui.calcDataTreeWidget.topLevelItem(i).text(4))
            calcDataSetting["calcData" + str(i + 1)]["secondData"] = self.ui.calcDataTreeWidget.topLevelItem(i).text(5)

            i += 1

        return calcDataSetting