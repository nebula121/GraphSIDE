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
from rawDataSetting import RawDataSettingWidget
from calcDataSetting import CalcDataSettingWidget

class DataSettingWidget(QDialog):
    
    def __init__(self, parent = None, dataSetSetting = {}):
        super(DataSettingWidget, self).__init__(parent)
        
        self.tempDataSetSetting = dataSetSetting

        self.ui = QUiLoader().load("./dataSetting.ui")

        self.raw = RawDataSettingWidget(dataSettingWidgetUi = self.ui, dataSetSetting = self.tempDataSetSetting)
        self.calc = CalcDataSettingWidget(dataSettingWidgetUi = self.ui, dataSetSetting = self.tempDataSetSetting)
        self.setupUi()
        

    def setupUi(self):
        self.ui.rawDataEnableButton.setEnabled(False)
        self.ui.calcDataEnableButton.setEnabled(False)
        
        self.ui.headerNumSpinBox.setValue(self.tempDataSetSetting["headerNum"])
        self.ui.headerNumSpinBox.setRange(0, 999)
        self.raw.setupUi()
        self.calc.setupUi()


    def getCurrentDataSetting(self):
        dataSetting = self.tempDataSetSetting
        dataSetting["headerNum"] = self.ui.headerNumSpinBox.value()
        dataSetting["rawData"] = self.raw.getCurrentRawDataSetting()
        dataSetting["calcData"] = self.calc.getCurrentCalcDataSetting()

        return dataSetting